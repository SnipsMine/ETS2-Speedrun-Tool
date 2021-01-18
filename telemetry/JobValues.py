from datetime import datetime
from dateutil.relativedelta import relativedelta


class JobValues:
    delivery_time = None
    cargo_value = None
    remaining_delivery_time = None
    city_destination = None
    city_destination_id = None
    company_destination = None
    company_destination_id = None
    city_source = None
    city_source_id = None
    company_source = None
    company_source_id = None
    income = None

    class Time:
        value = None
        date_time = None

        def calculate_date_time(self):
            if self.value:
                self.date_time = datetime.fromtimestamp(self.value * 60) - relativedelta(years=1969) - relativedelta(hours=1)
            else:
                pass
                # print("time value is Null")

        def calculate_remainng_time(self, delivery_time, game_time):
            if delivery_time > 0 and 0 < game_time < 4000000000:
                self.value = abs(delivery_time - game_time)

        def __str__(self):
            return f"{self.date_time}"


    class CargoValues:
        mass = None
        accessory_id = None
        id = None
        name = None

    def __init__(self):
        self.delivery_time = self.Time()
        self.cargo_value = self.CargoValues()
        self.remaining_delivery_time = self.Time()
