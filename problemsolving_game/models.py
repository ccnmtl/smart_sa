from django.db import models

# Create your models here.
from intervention.installed_games import InstalledGames,GameInterface

class ProblemSolvingGame(GameInterface):
    def pages(self):
        return ('video','my_issues','choose_one','problemsolve_one',)

    def template(self,page_id):
        game_context = {'mode':page_id,
                        'video':'video/problem_solving_complete.mov',
                        'width':320,
                        'height':196,
                        'needsvideo':(page_id in ('video','problemsolve_one')),
                        'videos':{'ask':'video/problem_solving01.mov',
                                  'aim':'video/problem_solving02.mov',
                                  'alternatives':'video/problem_solving03.mov',
                                  'action':'video/problem_solving04.mov',
                                  }

                        }
        if page_id == 'video':
            game_context['width'] = 426
            game_context['height'] = 256
        return ('problemsolving_game/my_issues.html',game_context)
    
    def variables(self,page_id=None):
        return ['problemsolving']

InstalledGames.register_game('problemsolving','Problem Solving', ProblemSolvingGame() )

