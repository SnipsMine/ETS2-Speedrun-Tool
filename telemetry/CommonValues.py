class CommonValues:
    scale = None
    game_time = None

    class GameTime:
        value = None

    def __init__(self):
        self.game_time = self.GameTime()
