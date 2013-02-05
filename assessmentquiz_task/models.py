from intervention.installed_games import InstalledGames, GameInterface


class AssessmentQuizTask(GameInterface):
    def __init__(self, mode):
        self.mode = mode

    def pages(self):
        return ('quiz',)

    def template(self, page_id):
        game_context = {'mode': self.mode}
        return ('assessmentquiz_task/%s.html' % self.mode, game_context)

    def variables(self, page_id=None):
        return ['assessmentquiz']

InstalledGames.register_game(
    'assessmentquiz',
    'Assessment Quiz Mood',
    AssessmentQuizTask('kten'))
InstalledGames.register_game(
    'assessmentquiz-audit',
    'Assessment Quiz Alchohol Audit',
    AssessmentQuizTask('audit'))
InstalledGames.register_game(
    'assessmentquiz-drug-audit',
    'Assessment Quiz Drug Audit',
    AssessmentQuizTask('drugaudit'))
