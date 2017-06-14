from smart_sa.intervention.installed_games import InstalledGames, GameInterface


class IslandGame(GameInterface):
    def __init__(self, mode):
        self.mode = mode

    def pages(self):
        return ('one',)

    def template(self, page_id):
        game_context = {'mode': self.mode}
        return ('island_game/island.html', game_context)


InstalledGames.register_game(
    'island', 'Island Before Medication', IslandGame('before-medication'))
InstalledGames.register_game(
    'island-after-medication', 'Island After Medication',
    IslandGame('after-medication'))
