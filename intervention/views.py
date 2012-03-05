# Create your views here.
from annoying.decorators import render_to
from django.template import RequestContext, loader, TemplateDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, QueryDict
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.conf import settings
from zipfile import ZipFile
from cStringIO import StringIO
from simplejson import dumps,loads
import os
import os.path
import random
from functools import wraps
from django.utils.decorators import available_attrs

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


def participant_required(function=None):
    def decorator(view_func):
        def get_participant(session):
            participant_id = session.get('participant_id',False)
            if not participant_id:
                return None
            try:
                p = Participant.objects.get(id=participant_id)
                return p
            except:
                return None

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            p = get_participant(request.session)
            if p is not None:
                request.participant = p
                return view_func(request, *args, **kwargs)
            path = request.get_full_path()
            set_participant_url = "/set_participant/?next=" + path
            return HttpResponseRedirect(set_participant_url)
        return _wrapped_view
    return decorator(function)

@render_to('intervention/set_participant.html')
@login_required    
def set_participant(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        id_number = request.POST.get('id_number','')
        try:
            p = Participant.objects.get(name=name)
            if p.id_number == id_number:
                request.session['participant_id'] = p.id
                return HttpResponseRedirect(request.POST.get('next','/intervention/'))
            else:
                return HttpResponse("id number does not match")
        except Participant.DoesNotExist:
            return HttpResponse("no participant with that name")
    # on a GET request, we make sure to clear it
    request.session.participant_id = ''
    return dict(next=request.GET.get('next','/intervention/'))

@render_to('intervention/intervention.html')
def intervention(request, intervention_id):
    return {'intervention' : get_object_or_404(Intervention, intervention_id=intervention_id),
            'offlineable' : True}

@render_to('intervention/counselor_landing_page.html')
@login_required
def counselor_landing_page(request):
    # if they come here, we want to clear out the participant from the session if any
    try:
        del request.session['participant_id']
    except KeyError:
        pass
    return dict(intervention=Intervention.objects.all()[0])

@render_to('intervention/manage_participants.html')
@login_required
def manage_participants(request):
    return dict(participants=Participant.objects.all(),
                counselors=User.objects.all())

@render_to('intervention/add_participant.html')
@login_required
def add_participant(request):
    if request.method == 'POST':
        p = Participant.objects.create(name=request.POST.get('name','unnamed'),
                                       id_number=request.POST.get('id_number',''),
                                       status=request.POST.get('status','') == 'on',
                                       defaulter=(request.POST.get('defaulter','') == 'on'),
                                       clinical_notes=request.POST.get('clinical_notes',''),
                                       )
        return HttpResponseRedirect("/manage/")
    else:
        return dict()

@login_required
def delete_participant(request,participant_id):
    # TODO: confirmation
    p = get_object_or_404(Participant,id=participant_id)
    p.delete()
    return HttpResponseRedirect("/manage/")

@render_to('intervention/edit_participant.html')
@login_required
def edit_participant(request,participant_id):
    p = get_object_or_404(Participant,id=participant_id)
    if request.method == 'POST':
        p.name = request.POST.get('name','')
        p.clinical_notes = request.POST.get('clinical_notes','')
        old_id_number = request.POST.get('old_id_number',False)
        new_id_number = request.POST.get('new_id_number',False)
        if old_id_number and new_id_number and old_id_number == p.id_number:
            p.id_number = new_id_number
        p.status = request.POST.get('status') == 'on'
        p.defaulter = request.POST.get('defaulter') == 'on'
        p.save()
        return HttpResponseRedirect("/manage/")
    return dict(participant=p)

@render_to('intervention/view_participant.html')
@login_required
def view_participant(request,participant_id):
    p = get_object_or_404(Participant,id=participant_id)
    return dict(participant=p)

@render_to('intervention/view_counselor.html')
@login_required
def view_counselor(request,counselor_id):
    c = get_object_or_404(User,id=counselor_id)
    return dict(counselor=c,
                notes=CounselorNote.objects.filter(counselor=c))

@render_to('intervention/ss/intervention.html')
@participant_required
@login_required
def ss_intervention(request, intervention_id):
    return dict(intervention=get_object_or_404(Intervention, id=intervention_id),
                participant=request.participant)

@render_to('intervention/ss/session.html')  
@participant_required
@login_required
def ss_session(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)
    participant=request.participant
    r = ParticipantSession.objects.filter(session=session,participant=participant)
    if r.count() == 0:
        ps = ParticipantSession.objects.create(session=session,participant=participant,
                                               status="incomplete")
    activities = session.activity_set.all()
    return dict(session=session, activities=activities,
                participant=request.participant)

@render_to('intervention/ss/activity.html')
@participant_required
@login_required
def ss_activity(request, activity_id):
    activity=get_object_or_404(Activity, pk=activity_id)
    participant=request.participant
    r = ParticipantActivity.objects.filter(activity=activity,participant=participant)
    if r.count() == 0:
        ps = ParticipantActivity.objects.create(activity=activity,participant=participant,
                                               status="incomplete")
    return dict(activity=activity,participant=request.participant)

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
    my_game = get_object_or_404(GamePage, pk=game_id)
    if not my_game.activity:
        """ for some reason, the database is littered with GamePage
         objects that don't have an activity associated with them 
         (and are therefore inaccessible normally) and googlebot 
         occasionally manages to pull them up, generating an exception
         I don't yet know if it's OK for these orphan gamepages to be in there
         so I'm hesitant to just delete them. In the meantime,
         if there is no referer (ie, probably googlebot or similar),
         we can silently ignore this exception 
         -Anders
         """
        if not request.META.get('HTTP_REFERER',None):
            return HttpResponse("orphan gamepage. please contact developers if you are seeing this")
    my_game.page_id = page_id
    template,game_context = my_game.template(page_id)
    
    t = loader.get_template(template)
    c = RequestContext(request,{
        'game' :  my_game,
        'game_context' : game_context,
        'offlineable' : True,
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

def all_uploads():
    root_len = len(settings.MEDIA_ROOT)
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            if f.endswith("~"):
                continue
            if "#" in f:
                continue
            if f.startswith("."):
                continue
            fullpath = os.path.join(root, f)
            archive_name = os.path.join("uploads",archive_root, f)
            public_path = os.path.join(settings.MEDIA_URL,archive_root,f)
            yield fullpath,f,archive_name,public_path

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
        for fullpath,f,archive_name,public_path in all_uploads():
            zipfile.write(fullpath, archive_name)                
    zipfile.close()

    resp = HttpResponse(buffer.getvalue())
    resp['Content-Disposition'] = "attachment; filename=masivukeni.zip" 
    return resp

def list_uploads(request):
    urls = []
    for fullpath,f,archive_name,public_path in all_uploads():
        url = "http://" + request.get_host() + public_path
        urls.append(url)
    return HttpResponse("\n".join(urls),content_type="text/plain")


