class NavigationValues:
    navigation_distance = None
    navigation_time = None
    speed_limit = None

    class SpeedLimit:
        value = None

    def __init__(self):
        self.speed_limit = self.SpeedLimit()
