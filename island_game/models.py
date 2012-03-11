from django.db import models

# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class IslandGame(GameInterface):
    def pages(self):
        return ('one',)

    def template(self,page_id):
        game_context = {}
        if page_id == 'one':
            return ('island_game/island.html',game_context)

InstalledGames.register_game('island','Island', IslandGame() )

