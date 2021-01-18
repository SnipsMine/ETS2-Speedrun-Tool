from telemetry.WheelConstants import WheelsConstants


class ConstantValues:
    wheel_constants = None
    motor_values = None
    capacity_values = None
    warning_factor_values = None
    brand_id = None
    brand = None
    id = None
    name = None

    class MotorValues:
        forward_gear_count = None
        reverse_gear_count = None
        retarder_step_count = None
        selector_count = None
        slot_handle_position = None
        slot_selectors = None
        slot_gear = None
        engine_rpm_max = None
        differential_ration = None
        gear_ratios_forward = None
        gear_ratios_reverse = None
        shifter_type_value = None

    class CapacityValues:
        fuel = None
        ad_blue = None

    class WarningFactorValues:
        fuel = None
        ad_blue = None
        air_pressure = None
        air_pressure_emergency = None
        oil_pressure = None
        water_temperature = None
        battery_voltage = None

    def __init__(self):
        self.wheel_constants = WheelsConstants()
        self.motor_values = self.MotorValues()
        self.capacity_values = self.CapacityValues()
        self.warning_factor_values = self.WarningFactorValues()
