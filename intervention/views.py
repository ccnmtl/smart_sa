# Create your views here.
from annoying.decorators import render_to
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
import random

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

def manifest_version(request):
    """ on development, we want to make sure the manifest gets updated every time. """
    if settings.DEBUG:
        return {'manifest_version': str(random.randint(0,320000))}
    else:
        # for production, we probably want a per-release kind of thing?
        # not really sure. will figure this out later.
        return {}

#VIEWS
def no_vars(request, template_name='intervention/blank.html'):
    t = loader.get_template(template_name)
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@render_to('intervention/intervention.html')
def intervention(request, intervention_id):
    return {'intervention' : get_object_or_404(Intervention, intervention_id=intervention_id),
            'offlineable' : True}

@render_to('intervention/session.html')  
def session(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)
    activities = session.activity_set.all()
    return {'session' : session, 'activities':activities,
            'offlineable' : True}

@render_to('intervention/activity.html')
def activity(request, activity_id):
    return { 'activity' : get_object_or_404(Activity, pk=activity_id) ,
             'offlineable' : True}

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
        'offlineable' : True,
    })
    return HttpResponse(t.render(c))

@render_to('intervention/session.html')
def test_session(request):
    intervention = Intervention(name='Test Intervention')
    session = ClientSession(intervention=intervention,
                            short_title = 'Test',
                            long_title = 'Test',
                            )
    activities = [{'id':'Test'+game_name,'short_title':label} for game_name,label in InstalledGames]
    return {
        'session' : session,
        'test':True,
        'activities':activities,
    }

@render_to('intervention/activity.html')
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
    return { 
        'activity' : activity,
        'test':True,
    }

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
@render_to('intervention/counselor_admin.html')
def smart_data(request):
    return {'hexkey':settings.FAKE_INTERVENTION_BACKUP_HEXKEY,
                                'hexiv':settings.FAKE_INTERVENTION_BACKUP_IV
            }

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
@render_to('intervention/upload_backup.html')
def save_backup_htmlupload(request):
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
            
    return {'errors':errors,
            'backups':previous_backups,
            }

#####################################
# ADMIN pages
#####################################

@permission_required('intervention.add_clientsession')
@render_to('intervention/admin/intervention_admin.html')
def intervention_admin(request, intervention_id):
    intervention = get_object_or_404(Intervention, intervention_id=intervention_id)
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
    return {'intervention' : intervention,'formset' : formset,}

@permission_required('intervention.add_clientsession')
@render_to('intervention/admin/session_admin.html')
def session_admin(request, session_id):
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
    return {'clientsession' : clientsession,'formset' : formset,}

#def as_sky(self):
#    "Returns this form rendered as HTML <p>s."
#    return self._html_output(u'<p class="hello">%(label)s %(field)s%(help_text)s</p>', u'%s', '</p>', u' %s', True)


@permission_required('intervention.add_clientsession')
@render_to('intervention/admin/activity_admin.html')
def activity_admin(request, activity_id):
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
    return {'activity' : activity,'formset' : formset,}

@permission_required('intervention.add_clientsession')
@render_to('intervention/admin/gamepage_admin.html')
def gamepage_admin(request, activity_id):
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
    return {'activity' : activity,'formset' : formset,}

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

def manifest(request):
    media_dir = os.path.join(os.path.dirname(__file__),"../media/")
    media_files = []
    for root, dirs, files in os.walk(media_dir):
        if "selenium" in root \
                or "mochikit/scripts" in root\
                or "mochikit/tests" in root\
                or "mochikit/doc" in root\
                or "mochikit/examples" in root\
                or "newskin" in root:
            continue
        for f in files:
            if f.endswith("~"):
                continue
            if "#" in f:
                continue
            if f.startswith("."):
                continue
            fullpath = os.path.join(root,f)
            path = "/site_media/" + fullpath[len(media_dir):]
            media_files.append(path)

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for f in files:
            if f.endswith("~"):
                continue
            if "#" in f:
                continue
            if f.startswith("."):
                continue
            # HTML5 appcache limits things to 5MB,
            # which our videos totally exceed.
            # need to find a way around this later, but for now:
            if f.endswith("mov"):
                continue

            fullpath = os.path.join(root,f)
            path = "/multimedia/" + fullpath[len(settings.MEDIA_ROOT):]
            media_files.append(path)

    dynamic_paths = ["/index.html","/home.html","/client_login.html",
                     "/help/credits.html","/help/backup.html",
                     "/masivukeni_admin_data.html"]
    for activity in Activity.objects.all():
        dynamic_paths.append("/activity%d_overview.html" % activity.id)
        for taskpage in activity.gamepage_set.all():
            dynamic_paths.append("/task/%s/%d%s.html" % (activity.game,taskpage.id,taskpage.page_name()))

    for session in ClientSession.objects.all():
        dynamic_paths.append("/session%d_agenda.html" % session.id)

    return HttpResponse("CACHE MANIFEST\n" + "\n".join(media_files + dynamic_paths),
                        content_type="text/cache-manifest")

