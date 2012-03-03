
# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class SSNMTreeGame(GameInterface):
    "Client will label the fruit, and then set disclosure and level of support info for each person"
    def pages(self):
        return ('addnames',)

    def template(self,page_id):
        game_context = {'mode':page_id}
        return ('ssnmtree_game/tree.html',game_context)
    
    def variables(self,page_id=None):
        return ['ssnmtree']

class SSNMTreeReview(SSNMTreeGame):
    "This is the '4th' part where the client reviews the tree with their friend"
    def pages(self):
        return ('review',)

InstalledGames.register_game('ssnmTree',
                             'Social Support Network Tree',
                             SSNMTreeGame())
InstalledGames.register_game('ssnmTreeReview',
                             'Social Support Network Review with Peer',
                             SSNMTreeReview())

