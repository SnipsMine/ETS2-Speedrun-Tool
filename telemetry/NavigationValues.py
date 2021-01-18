class NavigationValues:
    navigation_distance = None
    navigation_time = None
    speed_limit = None

    class Movement:
        value = None
        kph = None
        mph = None

        def calculate_speed(self):
            self.kph = self.value * 3.6
            self.mph = self.value * 2.25

    def __init__(self):
        self.speed_limit = self.Movement()
