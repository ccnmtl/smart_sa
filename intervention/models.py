"""
Intervention (e.g. SMART SA)
   ClientSessions (one day of activities), ordered
      Activities, ordered
         GamePage, ordered
         Instructions, ordered

NOTE: Jessica says there are no pages.  Games are not ordered within
pairs but 'to the side'.  Yei! much easier

Facts
   (User-Game-Key)
"""

from django.db import models
from django.contrib.auth.models import User
from intervention.installed_games import InstalledGames

class Intervention(models.Model):
    """SMART is an intervention--i.e. the top object"""
    name = models.CharField(max_length=200)
    intervention_id = models.CharField(max_length=8, default="1")
    general_instructions = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/intervention/%d/" % self.id

    def as_dict(self):
        clientsessions = [cs.as_dict() for cs in self.clientsession_set.all()]
        return dict(
            name=self.name,
            intervention_id=self.intervention_id,
            general_instructions=self.general_instructions,
            clientsessions=clientsessions,
            )

    def completed_all_sessions(self, participant):
        for cs in self.clientsession_set.all()[1:]:
            if cs.get_participant_status(participant) != "complete":
                return False
        return True

    def from_dict(self, d):
        self.name = d['name']
        self.general_instructions = d['general_instructions']
        self.intervention_id = d.get('intervention_id', str(self.id))
        self.save()
        self.clientsession_set.all().delete()
        for c in d['clientsessions']:
            cs = ClientSession.objects.create(
                intervention=self,
                short_title=c['short_title'],
                long_title=c['long_title'],
                introductory_copy=c['introductory_copy'],
                defaulter=c.get('defaulter',False),
                created=c['created'],
                modified=c['modified'],
                )
            cs.from_dict(c)

class ClientSession (models.Model):
    """One day of activities for a client"""
    intervention = models.ForeignKey(Intervention)
    
    short_title = models.CharField(max_length=512)
    long_title = models.CharField(max_length=512)
    introductory_copy = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    defaulter = models.BooleanField('only show to defaulters', default=False)

    class Meta:
        order_with_respect_to = 'intervention'
    
    def __unicode__(self):
        return self.short_title

    def get_absolute_url(self):
        return "/session/%d/" % self.id

    def index(self):
        "1-based index of the session"
        sessions = self.intervention.get_clientsession_order()
        if sessions:
            return 1+self.intervention.get_clientsession_order().index(self.id)
        else:
            return 1

    def as_dict(self):
        "nested dict of the data for json serializing"
        return dict(
            short_title=self.short_title,
            long_title=self.long_title,
            introductory_copy=self.introductory_copy,
            created=str(self.created),
            modified=str(self.modified),
            defaulter=self.defaulter,
            activities=[a.as_dict() for a in self.activity_set.all()],
            )

    def from_dict(self, d):
        "instantiate from a nested dict"
        self.short_title = d['short_title']
        self.long_title = d['long_title']
        self.introductory_copy = d['introductory_copy']
        self.created = d['created']
        self.modified = d['modified']
        self.defaulter = d.get('defaulter', False)
        self.save()
        self.activity_set.all().delete()
        for a in d['activities']:
            na = Activity.objects.create(
                clientsession=self,
                short_title=a['short_title'],
                long_title=a['long_title'],
                objective_copy=a['objective_copy'],
                created=a['created'],
                modified=a['modified'],
                game=a['game'],
                collect_notes=a.get('collect_notes',False),
                collect_buddy_name=a.get('collect_buddy_name',False),
                collect_referral_info=a.get('collect_referral_info',False),
                collect_reasons_for_returning=a.get('collect_reasons_for_returning',
                                                    False),
                )
            na.from_dict(a)

    def get_participant_status(self, participant):
        "has the participant completed this session, etc"
        r = self.participantsession_set.filter(participant=participant)
        if r.count() == 1:
            return r[0].status
        else:
            return ""

    def next(self):
        "next session in order"
        try:
            return self.get_next_in_order()
        except ClientSession.DoesNotExist:
            return None

    def completed_all_activities(self, participant):
        "has the participant completed all activities in this session"
        for a in self.activity_set.all()[1:]:
            if a.get_participant_status(participant) != "complete":
                return False
        return True


class Activity(models.Model):
    """Contains one or more pairs of instructions, and zero or one game.
    This can comprise multiple pairs.
    """
    class Meta:
        verbose_name_plural = "activities"
        order_with_respect_to = 'clientsession'
        
    clientsession = models.ForeignKey(ClientSession)
    
    short_title = models.CharField(max_length=512)
    long_title = models.CharField(max_length=512)
    objective_copy = models.TextField(blank=True)
    collect_notes = models.BooleanField(default=False)
    collect_buddy_name = models.BooleanField(default=False)
    collect_referral_info = models.BooleanField(default=False)
    collect_reasons_for_returning = models.BooleanField(default=False)
    
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    game = models.CharField(max_length=64, choices=InstalledGames, blank=True, null=True)
    
    def __unicode__(self):
        return self.short_title

    def get_absolute_url(self):
        return "/activity/%d/" % self.id

    def save(self, *args, **kwargs):
        "We want to precreate game pages, based on the game chosen"
        old_game_pages = tuple()
        if self._get_pk_val():
            old = Activity.objects.get(pk=self._get_pk_val())
            if old.game:
                old_game_pages = old.pages()

        super(Activity, self).save(*args, **kwargs)

        new_pages = tuple()
        if self.game:
            new_pages = self.pages()
        #we compare page tuples in case the game code itself changes
        #or two games are 'compatible' in page #'s etc.
        #may cause confusion.  we can change later
        if new_pages != old_game_pages:
            if old_game_pages != tuple():
                #delete old Game Pages? nah,
                for gamepage in GamePage.objects.filter(activity=self):
                    gamepage.activity = None
                    gamepage.save()
            if new_pages != tuple():
                for gamepage in new_pages:
                    GamePage.objects.create(activity=self)

    def index(self):
        "1-based index of activity wrt session"
        activities = self.clientsession.get_activity_order()
        if activities:
            return 1+self.clientsession.get_activity_order().index(self.id)
        else:
            return 1

    def next(self):
        "next activity in the session"
        try:
            return self.get_next_in_order()
        except Activity.DoesNotExist:
            return None

    def prev(self):
        "previous activity in the session"
        try:
            return self.get_previous_in_order()
        except Activity.DoesNotExist:
            return None

    #GAME code, we LOVE delegation!
    def pages(self):
        if self.game:
            return InstalledGames.pages(self.game)
        else:
            return tuple()

    def last_gamepage(self):
        if self.game:
            return self.pages()[-1]
        else:
            return None

    def last_gamepage_obj(self):
        if self.game:
            gamepages = list(self.gamepage_set.all())
            return gamepages[-1]
        else:
            return None

    def variables(self, page_id=None):
        if self.game:
            return InstalledGames.variables(self.game, page_id) or []
        return []

    def as_dict(self):
        "nested dict of content for json serialization"
        return dict(
            short_title=self.short_title,
            long_title=self.long_title,
            objective_copy=self.objective_copy,
            created=str(self.created),
            modified=str(self.modified),
            game=self.game,
            collect_notes=self.collect_notes,
            collect_buddy_name=self.collect_buddy_name,
            collect_referral_info=self.collect_referral_info,
            collect_reasons_for_returning=self.collect_reasons_for_returning,
            gamepages=[gp.as_dict() for gp in self.gamepage_set.all()],
            instructions=[i.as_dict() for i in self.instruction_set.all()],
        )
    def from_dict(self, d):
        "instantiate from a dict"
        self.short_title = d['short_title']
        self.long_title = d['long_title']
        self.objective_copy = d['objective_copy']
        self.created = d['created']
        self.modified = d['modified']
        self.game = d['game']
        self.collect_notes = d.get('collect_notes', False)
        self.collect_buddy_name = d.get('collect_buddy_name', False)
        self.collect_referral_info = d.get('collect_referral_info', False)
        self.collect_reasons_for_returning = d.get('collect_reasons_for_returning', False)
        self.save()
        self.gamepage_set.all().delete()
        for gp in d['gamepages']:
            ngp = GamePage.objects.create(
                activity=self,
                title=gp['title'],
                subtitle=gp['subtitle'],
                description=gp['description'],
                instructions=gp['instructions'],
                )
            ngp.from_dict(gp)
        self.instruction_set.all().delete()
        for i in d['instructions']:
            ni = Instruction.objects.create(
                activity=self,
                title=i['title'],
                style=i['style'],
                instruction_text=i['instruction_text'],
                help_copy=i['help_copy'],
                notes=i['notes'],
                image=i['image'],
                created=i['created'],
                modified=i['modified'],
                )
            ni.from_dict(i)

    def get_participant_status(self, participant):
        "has the participant completed the session, etc"
        r = self.participantactivity_set.filter(participant=participant)
        if r.count() == 1:
            return r[0].status
        else:
            return ""

class GamePage (models.Model):
    """A javascript 'game' associated with an activity."""
    #make null possible so 'deleting' is possible but recoverable
    activity  = models.ForeignKey(Activity, blank=True, null=True)
    class Meta:
        order_with_respect_to = 'activity'

    title = models.CharField(max_length=512, blank=True)
    subtitle = models.CharField(max_length=512, blank=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    page_id = None #blessed by view with name of the page

    def __unicode__(self):
        return self.title or self.page_id or str(self.id)

    def index(self):
        "1-based index"
        if self.page_id:
            return 1+list(self.activity.pages()).index(self.page_id)
        else:
            return 1+self.activity.get_gamepage_order().index(self.id)

    def page_name(self):
        return self.page_id or self.activity.pages()[self.index()-1]

    #we keep these methods separate from get_gamepage_order()
    #so they can work independent of a good DB (like in the test pages)
    def previous_url(self):
        "helper for prev nav in templates"
        ind = self.index()
        if ind > 1:
            try:
                id = str(self.get_previous_in_order().id)
            except:
                id = ''
            pages = self.activity.pages()
            return '%s/%s' % (id, pages[ind-2])
        else:
            return None
        
    def next_url(self):
        "helper for next nav in templates"
        pages = self.activity.pages()
        ind = self.index()
        if len(pages) > ind:
            try:
                id = str(self.get_next_in_order().id)
            except:
                id = ''
            return '%s/%s' % (id, pages[ind])
        else:
            return None

    def prev_title(self):
        "helper for prev nav in templates"
        try:
            return self.get_previous_in_order().title
        except:
            return ''

    def next_title(self):
        "helper for next nav in templates"
        try:
            return self.get_next_in_order().title
        except:
            return ''
    
    #GAME code, we LOVE delegation!
    def template(self, page_id):
        return InstalledGames.template(self.activity.game, page_id)

    def variables(self, page_id=None):
        return InstalledGames.variables(self.activity.game, page_id)

    def as_dict(self):
        "dict for serialization"
        return dict(
            title=self.title,
            subtitle=self.subtitle,
            description=self.description,
            instructions=self.instructions,
            )

    def from_dict(self, d):
        "instantiate from a dict"
        self.title = d['title']
        self.subtitle = d['subtitle']
        self.description = d['description']
        self.instructions = d['instructions']
        self.save()

class Instruction (models.Model):
    """A unit of interaction between facilitator and client
    Multiple per activity
    """
    activity = models.ForeignKey(Activity)

    class Meta:
        order_with_respect_to = 'activity'
    
    title = models.CharField(max_length=512, blank=True)
    STYLE_CHOICES = [('do', 'Do'), ('say', 'Say')]
    style = models.CharField(max_length=64, choices=STYLE_CHOICES, blank=True, null=True)
    instruction_text = models.TextField(blank=True)
    image = models.FileField(upload_to='intervention_images', blank=True, null=True)

    help_copy = models.TextField(blank=True)
    #image_path = models.CharField(max_length=300)
    notes = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)
    def __unicode__(self):
        return unicode(self.id)

    def index(self):
        "1-based index"
        return 1+self.activity.get_instruction_order().index(self.id)

    def as_dict(self):
        "return a dict for serializing"
        return dict(title=self.title,
                    style=self.style,
                    instruction_text=self.instruction_text,
                    help_copy=self.help_copy,
                    notes=self.notes,
                    image=str(self.image),
                    created=str(self.created),
                    modified=str(self.modified)
                    )
    def from_dict(self, d):
        "instantiate from a dict"
        self.title = d['title']
        self.style = d['style']
        self.instruction_text = d['instruction_text']
        self.help_copy = d['help_copy']
        self.notes = d['notes']
        self.image = d['image']
        self.created = d['created']
        self.modified = d['modified']
        self.save()

class Backup (models.Model):
    json_data = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    def save(self, *args, **kwargs):
        json.loads(self.json_data)
        super(Backup, self).save(*args, **kwargs)

    def as_dict(self):
        return dict(json_data=self.json_data,
                    created=str(self.created))

class Participant(models.Model):
    """ participant in the system """
    name = models.CharField(max_length=256)
    id_number = models.CharField(max_length=256)
    defaulter = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    clinical_notes = models.TextField(default="", blank=True)
    buddy_name = models.CharField(max_length=256, default="", blank=True)
    gender = models.CharField(max_length=16, default="male",
                              choices=[('male', 'Male'), ('female','Female')])

    # referral info fields
    initial_referral_mental_health = models.BooleanField(default=False)
    initial_referral_alcohol = models.BooleanField(default=False)
    initial_referral_drug_use = models.BooleanField(default=False)
    initial_referral_other = models.BooleanField(default=False)
    initial_referral_notes = models.TextField(default="", blank=True)

    defaulter_referral_mental_health = models.BooleanField(default=False)
    defaulter_referral_alcohol = models.BooleanField(default=False)
    defaulter_referral_drugs = models.BooleanField(default=False)
    defaulter_referral_other = models.BooleanField(default=False)
    defaulter_referral_notes = models.TextField(default="", blank=True)

    reasons_for_returning = models.TextField(default="", blank=True)

    def __unicode__(self):
        return self.name

    def to_json(self):
        "return a dict for serializing"
        return dict(
            name=self.name,
            id_number=self.id_number,
            defaulter=self.defaulter,
            status=self.status,
            clinical_notes=self.clinical_notes,
            buddy_name=self.buddy_name,
            gender=self.gender,
            initial_referral_mental_health=self.initial_referral_mental_health,
            initial_referral_alcohol=self.initial_referral_alcohol,
            initial_referral_drug_use=self.initial_referral_drug_use,
            initial_referral_other=self.initial_referral_other,
            initial_referral_notes=self.initial_referral_notes,
            defaulter_referral_mental_health=self.defaulter_referral_mental_health,
            defaulter_referral_alcohol=self.defaulter_referral_alcohol,
            defaulter_referral_drugs=self.defaulter_referral_drugs,
            defaulter_referral_other=self.defaulter_referral_other,
            defaulter_referral_notes=self.defaulter_referral_notes,
            reasons_for_returning=self.reasons_for_returning,
            game_vars=[{pgv.key : pgv.value} for pgv in self.participantgamevar_set.all()],
            session_progress=[dict(session="Session %d: %s" % (ps.session.index(), 
                                                               ps.session.long_title),
                                   status=ps.status,
                                   counselor_notes=[dict(counselor=cn.counselor.username, notes=cn.notes) 
                                                    for cn in ps.counselornote_set.all()],
                                   ) for ps in self.participantsession_set.all()],
            activity_progress=[dict(activity="Session %d: Activity %d: %s" % (pa.activity.clientsession.index(), 
                                                                              pa.activity.index(), pa.activity.long_title),
                                    status=pa.status) for pa in self.participantactivity_set.all()],
            )

    def save_game_var(self, key, value):
        "create or update a game variable"
        gv, created = ParticipantGameVar.objects.get_or_create(participant=self, key=key)
        gv.value = value
        gv.save()

    def get_game_var(self, key):
        "get a game variable's value"
        r = self.participantgamevar_set.filter(key=key)
        if r.count() == 0:
            return None
        else:
            return r[0].value

    def clear_all_data(self):
        """ this will mostly be called on the practice participant """
        self.participantsession_set.all().delete()
        self.participantactivity_set.all().delete()
        self.participantgamevar_set.all().delete()

    def is_practice(self):
        "template helper"
        return self.name == "practice"

    def display_name(self):
        if self.is_practice():
            return "Practice Participant"
        else:
            return self.name

    def next_session(self):
        """ which session the participant should be sent to """
        all_sessions = ClientSession.objects.all()

        if self.participantsession_set.count() == 0:
            # has not visited any sessions yet, 
            # so send them to the first one
            return all_sessions[0]

        complete_sessions = [ps.session for ps in self.participantsession_set.filter(status="complete").order_by("session___order")]
        incomplete_sessions = [ps.session for ps in self.participantsession_set.filter(status="incomplete").order_by("session___order")]

        if len(incomplete_sessions) > 0:
            # easy, just send them to the first incomplete session
            return incomplete_sessions[0]

        if len(complete_sessions) == len(all_sessions):
            # they have completed all sessions
            return None
        
        # if we make it here, it means they have some completed sesssions,
        # but haven't completed them all and there are no incomplete ones. 
        # so we get the last completed session and send them to the next
        return complete_session[-1].get_next()

    def next_activity(self):
        """ which activity the participant should be sent to """
        all_activities = Activity.objects.all()

        if self.participantactivity_set.count() == 0:
            # has not visited any activities yet, so send them to the first one
            return all_activities[0]

        paq = self.participantactivity_set.filter(status="complete").order_by("activity__clientsession___order","activity___order")
        complete_activities = [ps.activity for ps in paq]
        incomplete_activities = [ps.activity for ps in self.participantactivity_set.filter(status="incomplete").order_by("activity__clientsession___order","activity___order")]

        if len(incomplete_activities) > 0:
            # easy, just send them to the first incomplete activity
            return incomplete_activities[0]

        if len(complete_activities) == len(all_activities):
            # they have completed all activities
            return None
        
        # if we make it here, it means they have some completed sesssions,
        # but haven't completed them all and there are no incomplete ones. 
        # so we get the last completed activity and send them to the next
        return complete_activities[-1].get_next()


class ParticipantSession(models.Model):
    """ participant's progress on a session """
    participant = models.ForeignKey(Participant)
    session = models.ForeignKey(ClientSession)
    status = models.CharField(max_length=256, default="incomplete")

    def __unicode__(self):
        return "%s -> %s [%s]" % (self.participant.name, self.session.long_title, self.status)

    
class ParticipantActivity(models.Model):
    """ participant's progress on an activity """
    participant = models.ForeignKey(Participant)
    activity = models.ForeignKey(Activity)
    status = models.CharField(max_length=256, default="incomplete")

    def __unicode__(self):
        return "%s -> %s [%s]" % (self.participant.name, self.activity.long_title, self.status)


class CounselorNote(models.Model):
    """ notes entered by a counselor on a participant (for a particular session) """
    participantsession = models.ForeignKey(ParticipantSession)
    counselor = models.ForeignKey(User)
    notes = models.TextField(blank=True, null=True, default="")

    def __unicode__(self):
        return "%s <-- %s" % (self.participantsession.participant.name, self.counselor.username)

class ParticipantGameVar(models.Model):
    """ One game variable for a Participant"""
    participant = models.ForeignKey(Participant)
    key = models.CharField(max_length=256)
    value = models.TextField(default="", blank=True, null=True)

    def __unicode__(self):
        return "%s -> %s" % (self.participant.name, self.key)


class Deployment(models.Model):
    """ Singleton to track where this deployment is.

    Basically, the central one at masivukeni2.ccnmtl.columbia.edu should be
    "CCNMTL" and others will be the name of the clinic
    """
    name = models.CharField(max_length=256, default="Clinic")

    def is_online(self):
        "only one"
        return self.name == "CCNMTL"

    def is_clinic(self):
        "if not CCNMTL, must be a clinic"
        return self.name != "CCNMTL"
