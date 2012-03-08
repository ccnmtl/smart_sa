from django.db import models
from django.contrib.auth.models import User
from intervention.installed_games import InstalledGames
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

class Intervention(models.Model):
    """SMART is an intervention--i.e. the top object"""
    name = models.CharField(max_length=200)
    intervention_id = models.CharField(max_length=8,default="1")
    general_instructions = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/intervention/%d/" % self.id

    def as_dict(self):
        return dict(
            name=self.name,
            intervention_id=self.intervention_id,
            general_instructions=self.general_instructions,
            clientsessions=[cs.as_dict() for cs in self.clientsession_set.all()],
            )

    def from_dict(self,d):
        self.name = d['name']
        self.general_instructions = d['general_instructions']
        self.intervention_id = d.get('intervention_id',str(self.id))
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

    defaulter = models.BooleanField('only show to defaulters',default=False)

    class Meta:
        order_with_respect_to = 'intervention'
    
    def __unicode__(self):
        return self.short_title

    def get_absolute_url(self):
        return "/session/%d/" % self.id

    def index(self):
        sessions = self.intervention.get_clientsession_order()
        if sessions:
            return 1+self.intervention.get_clientsession_order().index(self.id)
        else:
            return 1

    def as_dict(self):
        return dict(
            short_title=self.short_title,
            long_title=self.long_title,
            introductory_copy=self.introductory_copy,
            created=str(self.created),
            modified=str(self.modified),
            defaulters=self.defaulter,
            activities=[a.as_dict() for a in self.activity_set.all()],
            )

    def from_dict(self,d):
        self.short_title = d['short_title']
        self.long_title = d['long_title']
        self.introductory_copy=d['introductory_copy']
        self.created = d['created']
        self.modified = d['modified']
        self.defaulter = d.get('defaulter',False)
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
                )
            na.from_dict(a)

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
    
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    game = models.CharField(max_length=64, choices=InstalledGames, blank=True,null=True)
    
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
        activities = self.clientsession.get_activity_order()
        if activities:
            return 1+self.clientsession.get_activity_order().index(self.id)
        else:
            return 1

    def next(self):
        try:
            return self.get_next_in_order()
        except Activity.DoesNotExist:
            return None

    def prev(self):
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

    def variables(self,page_id=None):
        if self.game:
            return InstalledGames.variables(self.game,page_id) or []
        return []

    def as_dict(self):
        return dict(
            short_title=self.short_title,
            long_title=self.long_title,
            objective_copy=self.objective_copy,
            created=str(self.created),
            modified=str(self.modified),
            game=self.game,
            collect_notes=self.collect_notes,
            gamepages=[gp.as_dict() for gp in self.gamepage_set.all()],
            instructions=[i.as_dict() for i in self.instruction_set.all()],
        )
    def from_dict(self,d):
        self.short_title = d['short_title']
        self.long_title = d['long_title']
        self.objective_copy = d['objective_copy']
        self.created = d['created']
        self.modified = d['modified']
        self.game = d['game']
        self.collect_notes = d.get('collect_notes',False)
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

class GamePage (models.Model):
    """A javascript 'game' associated with an activity."""
    #make null possible so 'deleting' is possible but recoverable
    activity  = models.ForeignKey(Activity,blank=True,null=True)
    class Meta:
        order_with_respect_to = 'activity'

    title = models.CharField(max_length=512,blank=True)
    subtitle = models.CharField(max_length=512,blank=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    page_id = None #blessed by view with name of the page

    def __unicode__(self):
        return self.title or self.page_id or str(self.id)

    def index(self):
        if self.page_id:
            return 1+list(self.activity.pages()).index(self.page_id)
        else:
            return 1+self.activity.get_gamepage_order().index(self.id)

    def page_name(self):
        return self.page_id or self.activity.pages()[self.index()-1]

    #we keep these methods separate from get_gamepage_order()
    #so they can work independent of a good DB (like in the test pages)
    def previous_url(self):
        ind = self.index()
        if ind > 1:
            try:
                id = str(self.get_previous_in_order().id)
            except:
                id = ''
            pages = self.activity.pages()
            return '%s%s' % (id,pages[ind-2])
        else:
            return None
        
    def next_url(self):
        pages = self.activity.pages()
        ind = self.index()
        if len(pages) > ind:
            try:
                id = str(self.get_next_in_order().id)
            except:
                id = ''
            return '%s%s' % (id,pages[ind])
        else:
            return None

    def prev_title(self):
        try:
            return self.get_previous_in_order().title
        except:
            return ''

    def next_title(self):
        try:
            return self.get_next_in_order().title
        except:
            return ''
    
    #GAME code, we LOVE delegation!
    def template(self, page_id):
        return InstalledGames.template(self.activity.game,page_id)

    def ss_template(self, page_id):
        return InstalledGames.ss_template(self.activity.game,page_id)

    def variables(self, page_id=None):
        return InstalledGames.variables(self.activity.game,page_id)

    def as_dict(self):
        return dict(
            title=self.title,
            subtitle=self.subtitle,
            description=self.description,
            instructions=self.instructions,
            )

    def from_dict(self,d):
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
    
    title = models.CharField(max_length=512,blank=True)
    STYLE_CHOICES = [('do','Do'),('say','Say'),]
    style = models.CharField(max_length=64, choices=STYLE_CHOICES,blank=True,null=True)
    instruction_text = models.TextField(blank=True)
    image = models.FileField(upload_to='intervention_images',blank=True,null=True)

    help_copy = models.TextField(blank=True)
    #image_path = models.CharField(max_length=300)
    notes = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)
    def __unicode__(self):
        return unicode(self.id)

    def index(self):
        return 1+self.activity.get_instruction_order().index(self.id)

    def as_dict(self):
        return dict(title=self.title,
                    style=self.style,
                    instruction_text=self.instruction_text,
                    help_copy=self.help_copy,
                    notes=self.notes,
                    image=str(self.image),
                    created=str(self.created),
                    modified=str(self.modified)
                    )
    def from_dict(self,d):
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
    def save(self,*args, **kwargs):
        import simplejson as json

        json.loads(self.json_data)
        #except ValueError:
        
        super(Backup, self).save(*args, **kwargs)

    def as_dict(self):
        return dict(json_data=self.json_data,
                    created=str(self.created))

class Fact (models.Model):
    """a piece of information connected to a client"""
    # user
    fact_key = models.CharField(max_length=100)
    fact_value = models.TextField(blank=True)
    help_copy = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)
    #activities = models.DateTimeField('date modified')
    def __unicode__(self):
        return self.fact_key

    def as_dict(self):
        return dict(fact_key=self.fact_key,
                    fact_value=self.fact_value,
                    help_copy=self.help_copy,
                    created=str(self.created),
                    modified=str(self.modified),
                    )

# These are the model objects that have been living client-side in localStorage/Gears

class Participant(models.Model):
    """ participant in the system """
    name = models.CharField(max_length=256)
    id_number = models.CharField(max_length=256)
    defaulter = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    clinical_notes = models.TextField(default="",blank=True)

    def save_game_var(self,key,value):
        gv,created = ParticipantGameVar.objects.get_or_create(participant=self,key=key)
        gv.value = value
        gv.save()

    def get_game_var(self,key):
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
        return self.name == "practice"

class ParticipantSession(models.Model):
    participant = models.ForeignKey(Participant)
    session = models.ForeignKey(ClientSession)
    status = models.CharField(max_length=256,default="incomplete")
    
class ParticipantActivity(models.Model):
    participant = models.ForeignKey(Participant)
    activity = models.ForeignKey(Activity)
    status = models.CharField(max_length=256,default="incomplete")

class CounselorNote(models.Model):
    participantsession = models.ForeignKey(ParticipantSession)
    counselor = models.ForeignKey(User)
    notes = models.TextField(blank=True,null=True,default="")

class ParticipantGameVar(models.Model):
    participant = models.ForeignKey(Participant)
    key = models.CharField(max_length=256)
    value = models.TextField(default="",blank=True,null=True)

class Deployment(models.Model):
    name = models.CharField(max_length=256,default="Clinic")

    def is_online(self):
        return self.name == "CCNMTL"

    def is_clinic(self):
        return self.name != "CCNMTL"
