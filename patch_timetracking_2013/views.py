"""
Main intervention views
"""
# Create your views here.
from annoying.decorators import render_to
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned
from django.utils import simplejson
from django.contrib.auth.models import User
from zipfile import ZipFile
from cStringIO import StringIO
from simplejson import dumps, loads
from datetime import datetime
import os
import os.path
from functools import wraps
from django.utils.decorators import available_attrs
from problemsolving_game.models import Issue
from intervention.models import Intervention
from pprint import pprint

from smart_sa.intervention.models import Participant, ClientSession, Activity
from smart_sa.intervention.models import Deployment, ParticipantSession, ParticipantActivity
from smart_sa.intervention.models import CounselorNote, GamePage, Backup, Instruction
from smart_sa.intervention.models import SessionVisit, ActivityVisit

# bump this if anything changes with Participant/Counselor serialization
API_VERSION = "002-2012-04-30"

# previous API Version Changes
# 001-2012-04-28 -> 002-2012-04-30 -- counselornotes are not per-session anymore

def inject_deployment(request):
    """injects the current Deployment into the context"""
    if Deployment.objects.count() == 0:
        return dict(deployment=Deployment.objects.create(name="Clinic"))
    else:
        return dict(deployment=Deployment.objects.all()[0])

#VIEWS
def no_vars(request, template_name='intervention/blank.html'):
    t = loader.get_template(template_name)
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def participant_required(function=None):
    def decorator(view_func):
        def get_participant(session):
            participant_id = session.get('participant_id', False)
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
            p = Participant.objects.get(name__iexact=name)
            if not p.status:
                return HttpResponse("this participant is marked as inactive")
            if p.id_number.lower() == id_number.lower():
                request.session['participant_id'] = p.id
                return HttpResponseRedirect(request.POST.get('next','/intervention/'))
            else:
                return HttpResponse("id number does not match")
        except Participant.DoesNotExist:
            return HttpResponse("no participant with that name")
    # on a GET request, we make sure to clear it
    request.session.participant_id = ''
    return dict(next=request.GET.get('next','/intervention/'))

@login_required
def clear_participant(request):
    try:
        del request.session['participant_id']
    except KeyError:
        pass
    return HttpResponseRedirect(request.GET.get('next','/intervention/'))

@login_required
def set_deployment(request):
    if request.POST:
        d = Deployment.objects.all()[0]
        d.name = request.POST.get('name','Clinic')
        d.save()
    return HttpResponseRedirect("/manage/")

@login_required
def start_practice_mode(request, intervention_id):
    p, created = get_or_create_first(Participant, name='practice')
    p.clear_all_data()
    request.session['participant_id'] = p.id
    return HttpResponseRedirect("/intervention/%d/" % int(intervention_id))

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
    return dict(participants=Participant.objects.all().order_by("name"),
                backups=Backup.objects.all().order_by("-created"),
                counselors=User.objects.all().order_by("username"))

@render_to('intervention/add_participant.html')
@login_required
def add_participant(request):
    if request.method == 'POST':
        if Participant.objects.filter(name=request.POST.get('name','unnamed')).count() > 0:
            return dict(error="A participant with this name already exists. Please chose a unique name",
                        form_data=request.POST)
        p = Participant.objects.create(name=request.POST.get('name','unnamed'),
                                       id_number=request.POST.get('id_number',''),
                                       status=request.POST.get('status','') == 'on',
                                       patient_id=request.POST.get('patient_id',''),
                                       defaulter=(request.POST.get('defaulter','') == 'on'),
                                       gender=request.POST.get('gender','male'),
                                       clinical_notes=request.POST.get('clinical_notes',''),
                                       )
        return HttpResponseRedirect("/manage/")
    else:
        return dict()

@login_required
def delete_participant(request, participant_id):
    # TODO: confirmation
    p = get_object_or_404(Participant, id=participant_id)
    p.delete()
    return HttpResponseRedirect("/manage/")

@render_to('intervention/edit_participant.html')
@login_required
def edit_participant(request, participant_id):
    p = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        p.name = request.POST.get('name', '')
        p.patient_id = request.POST.get('patient_id','')
        p.clinical_notes = request.POST.get('clinical_notes','')
        old_password = request.POST.get('password','')
        new_id_number = request.POST.get('new_id_number', '')
        if new_id_number != '' and old_password == p.id_number:
            p.id_number = new_id_number
        p.status = request.POST.get('status', '') == 'on'
        p.defaulter = request.POST.get('defaulter', '') == 'on'
        p.gender = request.POST.get('gender', 'male')
        p.save()
        return HttpResponseRedirect("/manage/")
    return dict(participant=p)

@render_to('intervention/edit_counselor.html')
@login_required
def edit_counselor(request, counselor_id):
    u = get_object_or_404(User, id=counselor_id)
    if request.method == 'POST':
        u.username = request.POST.get('username',u.username)
        u.is_active = request.POST.get('status',False)
        new_password = request.POST.get('new_password',"")
        if new_password != "":
            u.set_password(new_password)
        u.save()
        return HttpResponseRedirect("/manage/")
    return dict(counselor=u)

@render_to('intervention/view_participant.html')
@login_required
def view_participant(request, participant_id):
    p = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        password = request.POST['password']
        if p.id_number.lower() == password.lower():
            return dict(participant=p, all_interventions=Intervention.objects.all(), 
                        show_login_form=False)
        else:
            return HttpResponse("incorrect password. permission denied")
    else:
        return dict(participant=p, all_interventions=Intervention.objects.all(),
                    show_login_form=True)

@render_to('intervention/add_counselor.html')
@login_required
def add_counselor(request):
    if request.method == 'POST':
        u = User.objects.create(username=request.POST.get('username',''))
        u.set_password(request.POST.get('password',''))
        u.save()
        return HttpResponseRedirect("/manage/")
    else:
        return dict()

@render_to('intervention/report_index.html')
@login_required
def report_index(request):
    return dict()

@login_required
def participant_data_download(request):
    data = dict(deployment=Deployment.objects.all()[0].name)
    participants = []
    for p in Participant.objects.all():
        participants.append(p.to_json())

    data['participants'] = participants
    counselors = simplejson.loads(serializers.serialize("json", User.objects.all()))
    data['counselors'] = counselors
    data['API_VERSION'] = API_VERSION
    json = simplejson.dumps(data)
    resp = HttpResponse(json, content_type="application/json")
    clean_deployment_name = Deployment.objects.all()[0].name.lower().replace(" ","_")
    now = datetime.now()
    datestring = "%04d-%02d-%02dT%02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    resp['Content-Disposition'] = "attachment; filename=%s_%s_participant_data.json" % (clean_deployment_name, datestring)
    return resp

@login_required
def download_backup(request,backup_id):
    b = get_object_or_404(Backup,id=backup_id)
    json = b.json_data
    resp = HttpResponse(json, content_type="application/json")
    clean_deployment_name = b.deployment.lower().replace(" ","_")
    now = b.created
    datestring = "%04d-%02d-%02dT%02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    resp['Content-Disposition'] = "attachment; filename=%s_%s_participant_data.json" % (clean_deployment_name, datestring)
    return resp


@render_to("intervention/restore_participants.html")
@login_required
def restore_participants(request):
    logs = []
    if Deployment.objects.count() > 0:
        deployment = Deployment.objects.all()[0]
        if deployment.is_online():
            logs.append(dict(error="you should only use this feature on a clinic machine"))
            return dict(logs=logs)

    try:
        json_data = request.FILES['participants_data'].read()
        json = simplejson.loads(json_data)
    except Exception, e:
        logs.append(dict(error="invalid or corrupted data file: %s" % str(e)))
        return dict(logs=logs)

    # clear existing counselors (skipping the current user since 
    # they are an admin rather than a counselor and we don't want to log them out)
    User.objects.all().exclude(username=request.user.username).delete()
    logs.append(dict(info="existing counselors cleared"))
    # add counselors
    for counselor_data in json['counselors']:
        try:
            fields = counselor_data['fields']
            if fields['username'] == request.user.username:
                logs.append(dict(info="Admin account %s skipped" % fields['username']))
                # skip this user, since it's the admin doing the restore
                continue
            u = User.objects.create(
                username = fields['username'],
                first_name = fields['first_name'],
                last_name = fields['last_name'],
                password = fields['password'],
                is_active = fields['is_active'],
                is_superuser = fields['is_superuser'],
                is_staff = fields['is_staff'],
                last_login = fields['last_login'],
                email = fields['email'],
                date_joined = fields['date_joined'],
                )
            logs.append(dict(info="Counselor %s restored" % u.username))
        except Exception, e:
            logs.append(dict(warn="Could not restore counselor (%s): %s" % (str(e), str(counselor_data))))
    # delete existing participant data
    Participant.objects.all().delete()
    logs.append(dict(info="existing participant data cleared"))
    # update participants
    for p in json['participants']:
        try:
            np,plogs = Participant.from_json(p)
            logs.extend(plogs)
            logs.append(dict(info="Restored participant %s" % np.name))
        except Exception, e:
            logs.append(dict(warn="Could not fully restore participant (%s): %s" % (str(e), str(p))))

    return dict(logs=logs)
    
@render_to("intervention/upload_participants.html")
@login_required
def upload_participant_data(request):
    logs = []
    if Deployment.objects.count() > 0:
        deployment = Deployment.objects.all()[0]
        if not deployment.is_online():
            logs.append(dict(error="you should only use this feature on the CCNMTL deployment"))
            return dict(logs=logs)

    try:
        json_data = request.FILES['participants_data'].read()
        json = simplejson.loads(json_data)

    except Exception, e:
        logs.append(dict(error="invalid or corrupted data file: %s" % str(e)))
        return dict(logs=logs)

    b = Backup.objects.create(json_data=json_data,deployment=json['deployment'])
    return HttpResponse("participant data successfully backed up")


@login_required
def update_intervention_content(request):
    if Deployment.objects.count() > 0:
        deployment = Deployment.objects.all()[0]
        if deployment.is_online():
            return HttpResponse("you should only use this feature on a clinic machine")

    # TODO: read in chunks
    zc = request.FILES['intervention_content'].read()

#    uploads = TODO_get_list_of_uploads_from_zip()
    uploads = [] # TODO: handle uploads

    buffer = StringIO(zc)
    zipfile = ZipFile(buffer,"r")

    # Load Intervention objects
    json = loads(zipfile.read("interventions.json"))

    # clearing intervention prod database content...
    Intervention.objects.all().delete()

    # importing prod database content...
    for i in json['interventions']:
        intervention = Intervention.objects.create(name="tmp")
        intervention.from_dict(i)

    # Load Problem Solving objects
    json = loads(zipfile.read("issues.json"))

    # clearing problemsolving database content...
    Issue.objects.all().delete()

    # importing problemsolving prod database content...
    for i in json['issues']:
        issue = Issue.objects.create(name="tmp",ordinality=0)
        issue.from_dict(i)

    # updating uploaded files..."
    base_len = len(settings.PROD_MEDIA_BASE_URL)
    for upload in uploads:
        relative_path = upload[base_len:]
        relative_dir = os.path.join(*os.path.split(relative_path)[:-1])
        full_dir = os.path.join(settings.MEDIA_ROOT,relative_dir)
        try:
            os.makedirs(full_dir)
        except OSError:
            pass
        with open(os.path.join(settings.MEDIA_ROOT,relative_path),"w") as f:
            #   writing %s to %s" % (upload,relative_path)
            f.write(GET(upload))
    return HttpResponse("intervention content has been updated")

@render_to('intervention/intervention.html')
@participant_required
@login_required
def intervention(request, intervention_id):
    return dict(intervention=get_object_or_404(Intervention, id=intervention_id),
                participant=request.participant)

@render_to('intervention/testgen.html')
def testgen(request):
    return dict(interventions=Intervention.objects.all())

@render_to('intervention/session.html')  
@participant_required
@login_required
def session(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)
    participant = request.participant
    ps, created = get_or_create_first(ParticipantSession, session=session, participant=participant)
    activities = session.activity_set.all()
    return dict(session=session, activities=activities,
                participant=request.participant)

@participant_required
@login_required
def complete_session(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)

    if request.method == "POST":
        participant = request.participant
        ps, created = get_or_create_first(ParticipantSession, session=session, participant=participant)
        ps.status = "complete"
        ps.save()
        return HttpResponseRedirect(session.intervention.get_absolute_url())
    else:
        return HttpResponseRedirect(session.get_absolute_url())

def get_or_create_first(obj,**params):
    """ obj.get_or_create(), but handle duplicates by
    always using the first one returned.
    """
    try:
        return obj.objects.get_or_create(**params)
    except MultipleObjectsReturned:
        r = obj.objects.filter(**params)[0]
        return r, False

@participant_required
@login_required
def complete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if request.method == "POST":
        participant = request.participant
        pa, created = get_or_create_first(ParticipantActivity,activity=activity,participant=participant)
        pa.status = "complete"
        pa.save()
        if request.POST.get('counselor_notes', False):
            session = activity.clientsession
            ps, created = get_or_create_first(ParticipantSession,session=session, participant=participant)
            note, created = get_or_create_first(CounselorNote,participant=participant, counselor=request.user)
            note.notes = request.POST.get('counselor_notes', '')
            note.save()
        if request.POST.get('buddy_name', False):
            participant.buddy_name = request.POST.get('buddy_name', '')
            participant.save()
        if request.POST.get('reasons_for_returning', False):
            participant.reasons_for_returning = request.POST.get('reasons_for_returning', '')
            participant.save()

        if activity.collect_referral_info:
            if activity.clientsession.defaulter:
                participant.defaulter_referral_mental_health = request.POST.get('referral_mental_health', '')
                participant.defaulter_referral_alcohol = request.POST.get('referral_alcohol', '')
                participant.defaulter_referral_drug_use = request.POST.get('referral_drug_use', '')
                participant.defaulter_referral_other = request.POST.get('referral_other', '')
                participant.defaulter_referral_notes = request.POST.get('referral_notes', '')
            else:
                participant.initial_referral_mental_health = request.POST.get('referral_mental_health', '')
                participant.initial_referral_alcohol = request.POST.get('referral_alcohol', '')
                participant.initial_referral_drug_use = request.POST.get('referral_drug_use', '')
                participant.initial_referral_other = request.POST.get('referral_other', '')
                participant.initial_referral_notes = request.POST.get('referral_notes', '')
            participant.save()

        next_url = request.POST.get('next',None)
        if next_url:
            return HttpResponseRedirect(next_url)
        next_activity = activity.next()
        if activity.game:
            return HttpResponseRedirect("/task/%d/%s/" % (activity.gamepage_set.all()[0].id, activity.pages()[0]))
        else:
            if next_activity is None:
                return HttpResponseRedirect(activity.clientsession.get_absolute_url())
            else:
                return HttpResponseRedirect(next_activity.get_absolute_url())
    else:
        return HttpResponseRedirect(activity.get_absolute_url())


@render_to('intervention/activity.html')
@participant_required
@login_required
def activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    participant = request.participant
    ps, created = get_or_create_first(ParticipantSession, session=activity.clientsession, participant=participant)
    pa, created = get_or_create_first(ParticipantActivity, activity=activity, participant=participant)
    if not activity.game:
        # no game, so just loading the page should mark it complete
        pa.status = "complete"
        pa.save()
    cn, created = get_or_create_first(CounselorNote, participant=participant, counselor=request.user)
    counselor_notes = cn.notes
    return dict(activity=activity, participant=request.participant, counselor_notes=counselor_notes)

@participant_required
@login_required
def game(request, game_id, page_id):
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
        if not request.META.get('HTTP_REFERER', None):
            return HttpResponse("orphan gamepage. please contact developers if you are seeing this")

    my_game.page_id = page_id
    template, game_context = my_game.template(page_id)
    variables = []
    for k in my_game.variables(page_id):
        variables.append(dict(key=k, value=request.participant.get_game_var(k)))
    t = loader.get_template(template)
    c = RequestContext(request, {
        'game' :  my_game,
        'game_context' : game_context,
        'game_variables' : variables,
        'participant' : request.participant,
    })
    return HttpResponse(t.render(c))

@participant_required
@login_required
def save_game_state(request):
    if not request.method == "POST":
        return HttpResponse("must be a POST")
    try:
        json = loads(request.raw_post_data)
        for k in json.keys():
            request.participant.save_game_var(k, dumps(json[k]))
    except Exception, e:
        return HttpResponse("not ok")
    return HttpResponse("ok")


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
                    formset.cleaned_data[-1]['ORDER'] = 9999999

            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data, key=lambda x:x.get('ORDER')) if x!={}]
            intervention.set_clientsession_order(new_order)
    formset = ClientSessionFormSet(instance=intervention)
    return {'intervention' : intervention, 'formset' : formset,}

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
                    formset.cleaned_data[-1]['ORDER'] = 9999999
                    
            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data, key=lambda x:x.get('ORDER')) if x!={}]
            clientsession.set_activity_order(new_order)
            #refresh
            formset = ActivityFormSet(instance=clientsession)
    else:
        formset = ActivityFormSet(instance=clientsession)
    return {'clientsession' : clientsession, 'formset' : formset,}

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
            for i, new_object in enumerate(formset.new_objects):
                new_forms[i]['id'] = new_object
                if new_forms[i]['ORDER'] is None:
                    new_forms[i]['ORDER'] = 9999999 + new_object.id

            #after save, so we can order new elements
            new_order = [x.get('id').id for x in sorted(formset.cleaned_data, key=lambda x:x.get('ORDER')) if x!={}]
            activity.set_instruction_order(new_order)
            #refresh
            formset = InstructionFormSet(instance=activity)            
    else:
        formset = InstructionFormSet(instance=activity)
    return {'activity' : activity, 'formset' : formset,}

@permission_required('intervention.add_clientsession')
@render_to('intervention/admin/gamepage_admin.html')
def gamepage_admin(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    
    InstructionFormSet = inlineformset_factory(Activity, GamePage,
                                        fields=('instructions', 'title',
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
            archive_name = os.path.join("uploads", archive_root, f)
            public_path = os.path.join(settings.MEDIA_URL, archive_root, f)
            yield fullpath, f, archive_name, public_path

def content_zip(request):
    buffer = StringIO()
    zipfile = ZipFile(buffer,"w")
    zipfile.writestr("version.txt", "1")
    zipfile.writestr("interventions.json",
                     dumps(dict(interventions=[i.as_dict() for i in Intervention.objects.all()])))
    zipfile.writestr("issues.json",
                     dumps(dict(issues=[i.as_dict() for i in Issue.objects.all()])))

    if request.GET.get('include_uploads', False):
        for fullpath, f, archive_name, public_path in all_uploads():
            zipfile.write(fullpath, archive_name)                
    zipfile.close()

    return buffer.getvalue()

def content_sync(request):
    """ give the user a zip file of all the content for the intervention
    this means Intervention, ClientSession, etc objects in json format as well
    as all the images/videos that have been uploaded. 

    It does NOT include user data. 

    This is to enable a "pull content from production" command to update
    a developer's or staging database. Doing this since a lot of the functionality
    of the site is closely tied to content in the database.
    """
    resp = HttpResponse(content_zip(request))
    resp['Content-Disposition'] = "attachment; filename=masivukeni.zip" 
    return resp


def zip_download(request):
    """ same as content_sync, but puts a timestamp into the filename to make it nicer for a user to download """
    resp = HttpResponse(content_zip(request))
    now = datetime.now()
    datestring = "%04d-%02d-%02dT%02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    resp['Content-Disposition'] = "attachment; filename=masivukeni-%s.zip" % datestring
    return resp


def list_uploads(request):
    urls = []
    for fullpath, f, archive_name, public_path in all_uploads():
        url = "http://" + request.get_host() + public_path
        urls.append(url)
    return HttpResponse("\n".join(urls), content_type="text/plain")


@participant_required
@login_required
def log_session_visit(request, session_id):
    session = get_object_or_404(ClientSession, pk=session_id)
    participant = request.participant
    SessionVisit.objects.create(
        participant=participant,
        session=session)
    return HttpResponse("ok")


@participant_required
@login_required
def log_activity_visit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    participant = request.participant
    ActivityVisit.objects.create(
        participant=participant,
        activity=activity)
    return HttpResponse("ok")
