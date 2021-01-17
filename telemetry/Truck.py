from TruckConstants import ConstantValues
from TruckCurrent import CurrentValues
from TruckPositioning import Positioning


class TruckValues:

    constant_values = None
    current_values = None
    positioning = None

    def __init__(self):
        self.current_values = CurrentValues()
        self.constant_values = ConstantValues()
        self.positioning = Positioning()



