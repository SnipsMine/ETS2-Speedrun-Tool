from telemetry.Truck import TruckValues
from telemetry.TrailerValues import TrailerValues
from telemetry.CommonValues import CommonValues
from telemetry.ControlValues import ControlValues
from telemetry.JobValues import JobValues
from telemetry.NavigationValues import NavigationValues
from telemetry.SpecialEventsValues import SpecialEventsValues


class Telemetry:
    timestamp = None
    paused = None
    dll_version = None
    game_version = None
    game = None
    telemetry_version = None

    truck_values = None
    trailer_values = None
    common_values = None
    control_values = None
    job_values = None
    navigation_values = None
    special_events_values = None

    def __init__(self):
        self.truck_values = TruckValues()
        self.trailer_values = TrailerValues()
        self.common_values = CommonValues()
        self.control_values = ControlValues()
        self.job_values = JobValues()
        self.navigation_values = NavigationValues()
        self.special_events_values = SpecialEventsValues()

    class Version:
        major = None
        minor = None

        def get_version(self):
            return f"{self.major}.{self.minor}"
