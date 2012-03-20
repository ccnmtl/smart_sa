from django.db import models
from intervention.installed_games import InstalledGames,GameInterface

class Issue(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    ordinality = models.IntegerField()
    
    def __unicode__(self):
        return "%s) %s" % (self.ordinality, self.name) 
    
class ProblemSolvingGame(GameInterface):
    def pages(self):
        return ('barriers',)

    def template(self,page_id):
        game_context = { 'issues': Issue.objects.all().order_by('ordinality') }
        return ('problemsolving_game/problemsolving.html', game_context)
    
    def variables(self,page_id=None):
        return ['problemsolving']

InstalledGames.register_game('problemsolving','Problem Solving', ProblemSolvingGame())

