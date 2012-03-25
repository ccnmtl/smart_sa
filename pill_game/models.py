from intervention.installed_games import InstalledGames,GameInterface

class PillGame(GameInterface):
    def __init__(self, mode):
        self.mode = mode 

    def pages(self):
        return ('pills',)

    def template(self,page_id):
        game_context = {'mode':  self.mode}
        
        return ('pill_game/pill.html',game_context)
    
    def variables(self,page_id=None):
        return ['pill_game']

InstalledGames.register_game('pills', 'Pill Game - Practice', PillGame('practice'))
InstalledGames.register_game('pills-my-regimen', 'Pill Game - My Regimen', PillGame('actual'))

