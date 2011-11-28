# Create your views here.
from django.template import RequestContext, loader, TemplateDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from zipfile import ZipFile
from cStringIO import StringIO
from simplejson import dumps,loads
import os
import os.path

from aes_v001 import AESModeOfOperation,toNumbers,fromNumbers

from smart_sa.intervention.models import *

ENCRYPTION_ARGS = [AESModeOfOperation.modeOfOperation["OFB"], #mode
                   toNumbers(settings.INTERVENTION_BACKUP_HEXKEY),
                   AESModeOfOperation.aes.keySize['SIZE_256'],
                   toNumbers(settings.INTERVENTION_BACKUP_IV)
                   ]

#CUSTOM CONTEXT PROCESSOR
#see/set TEMPLATE_CONTEXT_PROCESSORS in settings_shared.py
#also note that we need RequestContext instead of the usual Context
def relative_root(request):
    """returns a string like '../../../' to get back to the root level"""
    from_top = request.path.count('/')-1
    relative_root_path = '../' * from_top
    return {'relative_root':relative_root_path,
            'INTERVENTION_MEDIA': relative_root_path + 'site_media/'
            }

#VIEWS
def no_vars(request, template_name='intervention/blank.html'):
    t = loader.get_template(template_name)
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def intervention(request, intervention_id):
    t = loader.get_template('intervention/intervention.html')
    c = RequestContext(request,{
        'intervention' : get_object_or_404(Intervention, intervention_id=intervention_id)
    })
    return HttpResponse(t.render(c))
  
def session(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)
    activities = session.activity_set.all()
    return render_to_response('intervention/session.html',
                              {'session' : session, 'activities':activities},
                              context_instance=RequestContext(request))

def activity(request, activity_id):
    t = loader.get_template('intervention/activity.html')
    c = RequestContext(request,{
        'activity' : get_object_or_404(Activity, pk=activity_id)
    })
    return HttpResponse(t.render(c))

def game(request, game_name, page_id, game_id=None):
    if not game_id:#for testing
        return test_task(request, game_name, page_id)
    my_game = get_object_or_404(GamePage, pk=game_id)
    my_game.page_id = page_id
    template,game_context = my_game.template(page_id)
    
    t = loader.get_template(template)
    c = RequestContext(request,{
        'game' :  my_game,
        'game_context' : game_context,
    })
    return HttpResponse(t.render(c))

def test_session(request):
    intervention = Intervention(name='Test Intervention')
    session = ClientSession(intervention=intervention,
                            short_title = 'Test',
                            long_title = 'Test',
                            )
    activities = [{'id':'Test'+game_name,'short_title':label} for game_name,label in InstalledGames]
    t = loader.get_template('intervention/session.html')
    c = RequestContext(request,{
        'session' : session,
        'test':True,
        'activities':activities,
    })
    return HttpResponse(t.render(c))

def test_activity(request, game_name):
    intervention = Intervention(name='Test Intervention')
    session = ClientSession(intervention=intervention,
                            short_title = 'Test '+game_name,
                            long_title = 'Test '+game_name,
                            )
    activity = Activity(id='Test'+game_name,
                        game=game_name,
                        short_title = game_name,
                        long_title = game_name,
                        clientsession = session
                        )
    t = loader.get_template('intervention/activity.html')
    c = RequestContext(request,{
        'activity' : activity,
        'test':True,
    })
    return HttpResponse(t.render(c))

def test_task(request, game_name, page_id):
    intervention = Intervention(name='Test Intervention')
    session = ClientSession(intervention=intervention,
                            short_title = 'Test '+game_name,
                            long_title = 'Test '+game_name,
                            )
    activity = Activity(id='Test'+game_name,
                        game=game_name,
                        short_title = game_name+' '+page_id,
                        long_title = game_name+' '+page_id,
                        clientsession = session
                        )
    my_game = GamePage(activity=activity,
                       title = 'Test Game Page '+page_id,
                       subtitle = 'Subtitle',
                       description = 'Ipso Lorem Description',
                       instructions = 'Ipso Lorem Instructions',
                       )
    my_game.page_id = page_id

    template,game_context = my_game.template(page_id)
    try:
        t = loader.get_template(template)
    except TemplateDoesNotExist:
        raise Http404('no template')
    c = RequestContext(request,{
        'game' :  my_game,
        'game_context' : game_context,
        'test':True,
    })
    return HttpResponse(t.render(c))
    


#####################################
# BACKUP/RESTORE pages
#####################################

#no login required.
def smart_data(request):
    t = loader.get_template('intervention/counselor_admin.html')
    c = RequestContext(request,{'hexkey':settings.FAKE_INTERVENTION_BACKUP_HEXKEY,
                                'hexiv':settings.FAKE_INTERVENTION_BACKUP_IV
                                })
    return HttpResponse(t.render(c))

@permission_required('intervention.add_backup')
def store_backup(request):
    if request.method == 'POST' and request.POST.has_key('backup'):
        try: #check that we got valid json
            Backup.objects.create(json_data=request.POST['backup'])
            return HttpResponse('ok')
        except ValueError:
            print 'not json'
            return HttpResponse('FAIL!')
        return HttpResponse('FAIL!')
    else:
        return HttpResponse('FAIL!')


@permission_required('intervention.add_backup')
def restore_from_backup(request):
    t = loader.get_template('intervention/restore.html')
    ctx = {}
    if request.GET.has_key('id'):
        backup = Backup.objects.get(pk=request.GET['id'])
        plaintext_json = backup.json_data
        moo = AESModeOfOperation()
        mode,orig_len,restoral_data = moo.encrypt(backup.json_data, *ENCRYPTION_ARGS)
        ctx = {'date_string':backup.created.strftime('%Y-%m-%d'),
               'restoral_data':fromNumbers(restoral_data),
               }
    c = RequestContext(request,ctx)
    response = HttpResponse(t.render(c))
    response['Content-Disposition'] = 'attachment; filename=restore.html'
    return response


@permission_required('intervention.add_backup')
def save_backup_htmlupload(request):
    t = loader.get_template('intervention/upload_backup.html')
    errors = ''

    if request.method == 'POST':
        if request.FILES.has_key('backup'):
            html_data = request.FILES['backup'].read()
            try:
                hex_ciphtext = html_data.split('<div id="data">').pop().split('</div>').pop(0)
                moo = AESModeOfOperation()
                plaintext_json = moo.decrypt(toNumbers(hex_ciphtext),None,*ENCRYPTION_ARGS)
                try:
                    Backup.objects.create(json_data=plaintext_json)
                    errors = 'Successfully saved the backup file'
                except:
                    errors = 'Unable to parse data correctly or save to the database.'
            except:
                errors = 'Unable to decrypt contents'

    previous_backups = Backup.objects.all()
            
    c = RequestContext(request,{'errors':errors,
                                'backups':previous_backups,
                                })
    return HttpResponse(t.render(c))    

#####################################
# ADMIN pages
#####################################

@permission_required('intervention.add_clientsession')
def intervention_admin(request, intervention_id):
    t = loader.get_template('intervention/admin/intervention_admin.html')
    intervention = get_object_or_404(Intervention, pk=intervention_id)
    ClientSessionFormSet = inlineformset_factory(Intervention, ClientSession,
                                                 can_delete=True,
                                                 can_order=True,
                                                 extra=1
                                                 )
    if request.method == 'POST':
        formset = ClientSessionFormSet(request.POST, request.FILES,
                                       instance=intervention)
        if formset.is_valid():
            formset.save()
            #prepare new objects for ordering
            if formset.new_objects:
                formset.cleaned_data[-1]['id'] = formset.new_objects[0]
                if formset.cleaned_data[-1]['ORDER'] is None:
                    formset.cleaned_data[-1]['ORDER']=9999999

            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data,key=lambda x:x.get('ORDER')) if x!={}]
            intervention.set_clientsession_order(new_order)
    formset = ClientSessionFormSet(instance=intervention)
    c = RequestContext(request,{'intervention' : intervention,'formset' : formset,})
    return HttpResponse(t.render(c))

@permission_required('intervention.add_clientsession')
def session_admin(request, session_id):
    t = loader.get_template('intervention/admin/session_admin.html')
    clientsession = get_object_or_404(ClientSession, pk=session_id)
    ActivityFormSet = inlineformset_factory(ClientSession, Activity,
                                            can_delete=True,
                                            can_order=True,
                                            extra=1
                                            )
    if request.method == 'POST':
        formset = ActivityFormSet(request.POST, request.FILES,
                                  instance=clientsession)
        if formset.is_valid():
            formset.save()
            #prepare new objects for ordering
            if formset.new_objects:
                formset.cleaned_data[-1]['id'] = formset.new_objects[0]
                if formset.cleaned_data[-1]['ORDER'] is None:
                    formset.cleaned_data[-1]['ORDER']=9999999
                    
            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data,key=lambda x:x.get('ORDER')) if x!={}]
            clientsession.set_activity_order(new_order)
            #refresh
            formset = ActivityFormSet(instance=clientsession)
    else:
        formset = ActivityFormSet(instance=clientsession)
    c = RequestContext(request,{'clientsession' : clientsession,'formset' : formset,})
    return HttpResponse(t.render(c))


#def as_sky(self):
#    "Returns this form rendered as HTML <p>s."
#    return self._html_output(u'<p class="hello">%(label)s %(field)s%(help_text)s</p>', u'%s', '</p>', u' %s', True)


@permission_required('intervention.add_clientsession')
def activity_admin(request, activity_id):
    t = loader.get_template('intervention/admin/activity_admin.html')
    activity = get_object_or_404(Activity, pk=activity_id)
    InstructionFormSet = inlineformset_factory(Activity, Instruction,
                                        can_delete=True,
                                        can_order=True,
                                        fields=('title',
                                                'style',
                                                'instruction_text',
                                                'image',
                                                ),
                                        extra=3
                                        )
    if request.method == 'POST':
        formset = InstructionFormSet(request.POST, request.FILES,
                              instance=activity)
        if formset.is_valid():
            formset.save()
            #prepare new objects for ordering
            #more complicated than session,intervention because we have 3
            new_forms = [f.cleaned_data for f in formset.forms[-3:] if f.has_changed()]
            for i,new_object in enumerate(formset.new_objects):
                new_forms[i]['id'] = new_object
                if new_forms[i]['ORDER'] is None:
                    new_forms[i]['ORDER']=9999999+new_object.id

            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data,key=lambda x:x.get('ORDER')) if x!={}]
            activity.set_instruction_order(new_order)
            #refresh
            formset = InstructionFormSet(instance=activity)            
    else:
        formset = InstructionFormSet(instance=activity)
    c = RequestContext(request,{'activity' : activity,'formset' : formset,})
    return HttpResponse(t.render(c))

@permission_required('intervention.add_clientsession')
def gamepage_admin(request, activity_id):
    t = loader.get_template('intervention/admin/gamepage_admin.html')
    activity = get_object_or_404(Activity, pk=activity_id)
    
    InstructionFormSet = inlineformset_factory(Activity, GamePage,
                                        fields=('instructions','title',
                                                ),
                                        can_delete=False,
                                        extra=0
                                        )
    if request.method == 'POST':
        formset = InstructionFormSet(request.POST, request.FILES,
                              instance=activity)
        if formset.is_valid():
            formset.save()
    else:
        formset = InstructionFormSet(instance=activity)
    c = RequestContext(request,{'activity' : activity,'formset' : formset,})
    return HttpResponse(t.render(c))





def content_sync(request):
    """ give the user a zip file of all the content for the intervention
    this means Intervention, ClientSession, etc objects in json format as well
    as all the images/videos that have been uploaded. 

    It does NOT include user data. 

    This is to enable a "pull content from production" command to update
    a developer's or staging database. Doing this since a lot of the functionality
    of the site is closely tied to content in the database.
    """

    buffer = StringIO()
    zipfile = ZipFile(buffer,"w")
    zipfile.writestr("version.txt", "1")
    zipfile.writestr("interventions.json",
                     dumps(dict(interventions=[i.as_dict() for i in Intervention.objects.all()])))

    if request.GET.get('include_uploads',False):
        root_len = len(settings.MEDIA_ROOT)
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            archive_root = os.path.abspath(root)[root_len:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join("uploads",archive_root, f)
                zipfile.write(fullpath, archive_name)    
    zipfile.close()

    resp = HttpResponse(buffer.getvalue())
    resp['Content-Disposition'] = "attachment; filename=masivukeni.zip" 
    return resp

def list_uploads(request):
    urls = []
    root_len = len(settings.MEDIA_ROOT)
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            url = "http://" + request.get_host() + os.path.join(settings.MEDIA_URL,archive_root,f)
            urls.append(url)
    return HttpResponse("\n".join(urls),content_type="text/plain")
