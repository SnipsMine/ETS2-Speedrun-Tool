class ControlValues:

    input_values = None
    game_values = None

    class InputValues:
        steering = None
        Throttle = None
        brake = None
        clutch = None

    class GameValues:
        steering = None
        throttle = None
        brake = None
        clutch = None

    def __init__(self):
        self.input_values = self.InputValues()
        self.game_values = self.GameValues()
