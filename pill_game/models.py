from django.db import models

# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class PillGame(GameInterface):
    def pages(self):
        return ('choose_treatment_line','highlight_meds', 'drop_into_bins')

    def template(self,page_id):
        game_context = {'mode':page_id }
        
        page_game = {'choose_treatment_line': 'choose_treatment_line',
        'highlight_meds': 'highlight_meds', 
        'drop_into_bins': 'drop_into_bins'
        }
        return ('pill_game/%s.html' % page_game.get(page_id,'choose_treatment_line') ,game_context)
    
    def variables(self,page_id=None):
        return ['pill_game']

InstalledGames.register_game('pills','Pills',PillGame())

