import re


class GameInterface:
    """This class is meant to be the parent for game application
    """
    def pages(self):
        return ('page_one',)

    def template(self, page_id):
        game_context = {'page_id': page_id}
        return ('intervention/game.html', game_context)

    def variables(self, page_id=None):
        """return a list of strings to declare the variables you will
        store/retrieve
        If your variable name conflicts with another game, you will share state
        """
        return []


class InstalledGamesLazySingleton:
    GAMES_INSTALLED = []
    GAME_OBJECTS = dict()

    def register_game(self, game_code, view_name, game_obj):
        if game_code not in self.GAME_OBJECTS:
            self.GAMES_INSTALLED.append((game_code, view_name, ))
            self.GAME_OBJECTS[game_code] = game_obj

        for p in game_obj.pages():
            if re.findall('\W', p):
                raise ("Game pages must have only word "
                       "(web friendly) characters.")

    def __iter__(self):
        return iter(self.GAMES_INSTALLED)

    # more delegation, 2nd round
    def pages(self, game_code):
        return self.GAME_OBJECTS[game_code].pages()

    def template(self, game_code, page_id):
        return self.GAME_OBJECTS[game_code].template(page_id)

    def variables(self, game_code, page_id=None):
        return self.GAME_OBJECTS[game_code].variables(page_id)


InstalledGames = InstalledGamesLazySingleton()
