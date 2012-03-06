from django.db import models

# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class AssessmentQuizTask(GameInterface):
    def pages(self):
        return ('kten','audit')

    def template(self,page_id):
        game_context = {'mode':page_id,}
        return ('assessmentquiz_task/%s.html' % page_id ,game_context)

    def ss_template(self,page_id):
        game_context = {'mode':page_id,}
        return ('assessmentquiz_task/ss_%s.html' % page_id ,game_context)
    
    def variables(self,page_id=None):
        return ['assessmentquiz']

InstalledGames.register_game('assessmentquiz','Assessment Quiz', AssessmentQuizTask() )

