from telemetry.WheelValues import WheelValues


class CurrentValues:
    wheel_values = None
    motor_values = None
    dashboard_values = None
    light_values = None
    damage_values = None
    electric_enabled = None
    engine_enabled = None
    position_value = None
    acceleration_values = None

    class MotorValues:
        gear_values = None
        brake_values = None

        class GearValues:
            h_shifter_slot = None
            selected = None
            h_shifter_selector = None

        class BrakeValues:
            retarder_level = None
            airPressure = None
            temperature = None
            parking_brake = None
            motor_brake = None

        def __init__(self):
            self.gear_values = self.GearValues()
            self.brake_values = self.BrakeValues()

    class DashboardValues:
        gear_dashboards = None
        rpm = None
        ad_blue = None
        oil_pressure = None
        oil_temperature = None
        water_temperature = None
        battery_voltage = None
        odometer = None
        wipers = None
        cruise_control = None

        speed = None
        cruise_control_speed = None
        fuel_value = None
        warning_values = None

        class Movement:
            value = None
            kph = None
            mph = None

            def calculate_speed(self):
                self.kph = self.value * 3.6
                self.mph = self.value * 2.25

        class FuelValue:
            amount = None
            average_consumption = None
            range = None

        class WarningValues:
            air_pressure = None
            air_pressure_emergency = None
            fuel_w = None
            ad_blue = None
            oil_pressure = None
            water_pressure = None
            battery_voltage = None

        def __init__(self):
            self.speed = self.Movement()
            self.cruise_control_speed = self.Movement()
            self.fuel_value = self.FuelValue()
            self.warning_values = self.WarningValues()

    class LightValues:
        aux_front = None
        aux_roof = None
        dashboard_back_light = None
        blinker_left_active = None
        blinker_right_active = None
        blinker_left_on = None
        blinker_right_on = None
        parking = None
        beam_low = None
        beam_high = None
        beacon = None
        brake = None
        reverse = None

    class DamageValues:
        engine = None
        transmission = None
        cabin = None
        chassis = None
        wheelsAvg = None

    class AccelerationValues:
        linear_velocity = None
        angular_velocity = None
        linear_acceleration = None
        angular_acceleration = None
        cabin_angular_velocity = None
        cabin_angular_acceleration = None

    def __init__(self):
        self.wheel_values = WheelValues()
        self.motor_values = self.MotorValues()
        self.dashboard_values = self.DashboardValues()
        self.light_values = self.LightValues()
        self.damage_values = self.DamageValues()
        self.acceleration_values = self.AccelerationValues()
