from telemetry.TruckConstants import ConstantValues
from telemetry.TruckCurrent import CurrentValues
from telemetry.TruckPositioning import Positioning


class TruckValues:

    constant_values = None
    current_values = None
    positioning = None

    def __init__(self):
        self.current_values = CurrentValues()
        self.constant_values = ConstantValues()
        self.positioning = Positioning()



