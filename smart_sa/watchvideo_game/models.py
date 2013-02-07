from smart_sa.intervention.installed_games import InstalledGames, GameInterface


class WatchVideoGame1(GameInterface):
    "Client will watch a video"
    def pages(self):
        return ('soldiers_snakes', )

    def template(self, page_id):
        game_context = {
            'video': 'video/%s.mp4' % page_id,
            'width': 530,  # 320,
            'height': 413,  # 255,
            }
        return ('watchvideo_game/video.html', game_context)

    def variables(self, page_id=None):
        return []


class WatchVideoGame2(WatchVideoGame1):
    "watch another video"
    def pages(self):
        return ('joseph_hope', )


class WatchVideoGame3(WatchVideoGame1):
    "watch another video"
    def pages(self):
        return ('problem_solving_smart_sa_new_vo', )

InstalledGames.register_game('video-soldiers',
                             'Soldiers and Snakes',
                             WatchVideoGame1())
InstalledGames.register_game('video-joseph',
                             'Joseph and Hope',
                             WatchVideoGame2())
InstalledGames.register_game('video-problem-solving',
                             'Problem Solving Video',
                             WatchVideoGame3())
