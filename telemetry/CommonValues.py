from datetime import datetime
from dateutil.relativedelta import relativedelta


class CommonValues:
    scale = None

    game_time = None
    next_rest_stop = None
    next_rest_stop_time = None

    class Time:
        value = None
        date_time = None

        def calculate_date_time(self):
            self.date_time = datetime.fromtimestamp(self.value*60) - relativedelta(years=1969) - relativedelta(hours=1)

        def __str__(self):
            return f"{self.date_time}"

    def __init__(self):
        self.game_time = self.Time()
        self.next_rest_stop = self.Time()
        self.next_rest_stop_time = self.Time()

    def calculate_next_rest_stop_time(self):
        self.next_rest_stop_time.value = self.game_time.value + self.next_rest_stop.value