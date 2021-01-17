from WheelValues import WheelValues
from WheelConstants import WheelsConstants


class TrailerValues:
    damage = None
    attached = None
    position = None
    id = None

    wheel_values = None
    wheel_constants = None
    acceleration_values = None

    class AccelerationValues:
        linear_velocity = None
        angular_velocity = None
        linear_acceleration = None
        angular_acceleration = None

    def __init__(self):
        self.wheel_values = WheelValues()
        self.wheel_constants = WheelsConstants()
        self.acceleration_values = self.AccelerationValues()
