from django.db import models
from smart_sa.intervention.installed_games import InstalledGames, GameInterface


class Issue(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    ordinality = models.IntegerField()
    subtext = models.CharField(max_length=1000, null=True, blank=True)
    example = models.CharField(max_length=1000, null=True, blank=True)

    def as_dict(self):
        return dict(
            name=self.name,
            text=self.text,
            ordinality=self.ordinality,
            subtext=self.subtext,
            example=self.example
        )

    def from_dict(self, d):
        self.name = d['name']
        self.text = d['text']
        self.ordinality = d['ordinality']
        self.subtext = d['subtext']
        self.example = d['example']
        self.save()

    def __unicode__(self):
        return "%s) %s" % (self.ordinality, self.name)


class ProblemSolvingGame(GameInterface):
    def pages(self):
        return ('barriers', )

    def template(self, page_id):
        game_context = {'issues': Issue.objects.all().order_by('ordinality')}
        return ('problemsolving_game/problemsolving.html', game_context)

    def variables(self, page_id=None):
        return ['problemsolving']


InstalledGames.register_game(
    'problemsolving',
    'Problem Solving', ProblemSolvingGame())
