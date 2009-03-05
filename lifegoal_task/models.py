from django.db import models

# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class LifeGoalsTask(GameInterface):
    def pages(self):
        return ('goals',)

    def template(self,page_id):
        game_context = {'mode':page_id,}
        return ('lifegoal_task/goals.html',game_context)
    
    def variables(self,page_id=None):
        return ['lifegoals']

InstalledGames.register_game('lifegoals','Life Goals', LifeGoalsTask() )

