from django.db import models
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
    general_instructions = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class ClientSession (models.Model):
    """One day of activities for a client"""
    intervention = models.ForeignKey(Intervention)
    
    short_title = models.CharField(max_length=512)
    long_title = models.CharField(max_length=512)
    introductory_copy = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    class Meta:
        order_with_respect_to = 'intervention'
    
    def __unicode__(self):
        return self.short_title
    def index(self):
        sessions = self.intervention.get_clientsession_order()
        if sessions:
            return 1+self.intervention.get_clientsession_order().index(self.id)
        else:
            return 1

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
    
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)

    game = models.CharField(max_length=64, choices=InstalledGames, blank=True,null=True)
    
    def __unicode__(self):
        return self.short_title

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

    def variables(self, page_id=None):
        return InstalledGames.variables(self.activity.game,page_id)

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
    image = models.ImageField(upload_to='intervention_images',blank=True,null=True)

    help_copy = models.TextField(blank=True)
    #image_path = models.CharField(max_length=300)
    notes = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)
    def __unicode__(self):
        return unicode(self.id)

    def index(self):
        return 1+self.activity.get_instruction_order().index(self.id)

class Backup (models.Model):
    json_data = models.TextField(blank=True)
    created = models.DateTimeField('date created', auto_now_add=True)
    def save(self,*args, **kwargs):
        import simplejson as json

        json.loads(self.json_data)
        #except ValueError:
        
        super(Backup, self).save(*args, **kwargs)

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
