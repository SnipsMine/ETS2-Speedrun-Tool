from mmap import mmap
from telemetry import Telemetry, Vector, Placement, Euler

import struct

GAME = ['unknown', "Euro Truck Simulator 2", "American Truck Simulator"]
AUX_LEVEL = ['Off', 'Dimmed', 'Full']
SHIFTER_TYPE = ["arcade", "automatic", "manual", "hshifter"]


class ProcessMMF:
    file_name = None
    file_size = None
    mm = None

    offset = None
    offset_area = None
    offset_areas = (0, 40, 500, 700, 1800, 2000, 2600, 2800, 3000, 4800, 5000, 5200, 6800)

    string_size = 64
    wheel_size = 16

    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size
        self.mm = self.open_mmf()

    def open_mmf(self):
        return mmap(0, self.file_size, self.file_name)

    def close_mmf(self):
        self.mm.close()

    def parse_mmf(self):
        self.offset_area = 0
        self.set_offset()
        data = Telemetry()

        self.first_area(data)
        self.second_area(data)
        self.third_area(data)
        self.fourth_area(data)
        self.fifth_area(data)
        self.sixth_area(data)
        self.seventh_area(data)
        self.eighth_area(data)
        self.ninth_area(data)
        self.tenth_area(data)
        self.eleventh_area(data)

        return data

    def first_area(self, data):
        data.timestamp = self.get_uint()
        data.paused = self.get_bool()

        self.next_area()

    def second_area(self, data):
        # Second area
        data.dll_version = self.get_uint()
        version = data.Version()

        version.major = self.get_uint()
        version.minor = self.get_uint()
        data.game_version = version.get_version()

        data.game = GAME[self.get_uint()]

        version = data.Version()
        version.major = self.get_uint()
        version.minor = self.get_uint()
        data.telemetry_version = version.get_version()

        # Get game time
        game_time = self.get_uint()
        data.common_values.game_time.value = game_time
        data.common_values.game_time.calculate_date_time()

        data.truck_values.constant_values.motor_values.forward_gear_count = self.get_uint()
        data.truck_values.constant_values.motor_values.reverse_gear_count = self.get_uint()
        data.truck_values.constant_values.motor_values.retarder_step_count = self.get_uint()
        data.truck_values.constant_values.wheel_constants.count = self.get_uint()
        data.truck_values.constant_values.motor_values.selector_count = self.get_uint()

        # Get job delivery
        delivery_time = self.get_uint()
        data.job_values.delivery_time.value = delivery_time
        data.job_values.delivery_time.calculate_date_time()

        # Set remaining delivery time
        data.job_values.remaining_delivery_time.calculate_remainng_time(delivery_time, game_time)
        data.job_values.remaining_delivery_time.calculate_date_time()

        data.trailer_values.wheel_constants.count = self.get_uint()

        data.truck_values.current_values.motor_values.gear_values.h_shifter_slot = self.get_uint()
        data.truck_values.current_values.motor_values.brake_values.retarder_level = self.get_uint()
        data.truck_values.current_values.light_values.aux_front = AUX_LEVEL[self.get_uint()]
        data.truck_values.current_values.light_values.aux_roof = AUX_LEVEL[self.get_uint()]
        data.trailer_values.wheel_values.substance = self.get_uint_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.substance = self.get_uint_array(self.wheel_size)

        data.truck_values.constant_values.motor_values.slot_handle_position = self.get_uint_array(32)
        data.truck_values.constant_values.motor_values.slot_selectors = self.get_uint_array(32)

        self.next_area()

    def third_area(self, data):
        # Get next rest stop
        data.common_values.next_rest_stop.value = abs(self.get_int())
        data.common_values.next_rest_stop.calculate_date_time()

        data.common_values.calculate_next_rest_stop_time()
        data.common_values.next_rest_stop_time.calculate_date_time()

        data.truck_values.current_values.motor_values.gear_values.selected = self.get_int()
        data.truck_values.current_values.dashboard_values.gear_dashboards = self.get_int()
        data.truck_values.constant_values.motor_values.slot_gear = self.get_int_array(32)

        self.next_area()

    def fourth_area(self, data):
        data.common_values.scale = self.get_float()
        data.truck_values.constant_values.capacity_values.fuel = self.get_float()
        data.truck_values.constant_values.warning_factor_values.fuel = self.get_float()
        data.truck_values.constant_values.capacity_values.ad_blue = self.get_float()
        data.truck_values.constant_values.warning_factor_values.ad_blue = self.get_float()
        data.truck_values.constant_values.warning_factor_values.air_pressure = self.get_float()
        data.truck_values.constant_values.warning_factor_values.air_pressure_emergency = self.get_float()
        data.truck_values.constant_values.warning_factor_values.oil_pressure = self.get_float()
        data.truck_values.constant_values.warning_factor_values.water_temperature = self.get_float()
        data.truck_values.constant_values.warning_factor_values.battery_voltage = self.get_float()
        data.truck_values.constant_values.motor_values.engine_rpm_max = self.get_float()
        data.truck_values.constant_values.motor_values.differential_ration = self.get_float()
        data.job_values.cargo_value.mass = self.get_float()
        data.truck_values.constant_values.wheel_constants.radius = self.get_float_array(self.wheel_size)
        data.trailer_values.wheel_constants.radius = self.get_float_array(self.wheel_size)
        data.truck_values.constant_values.motor_values.gear_ratios_forward = self.get_float_array(24)
        data.truck_values.constant_values.motor_values.gear_ratios_reverse = self.get_float_array(8)

        # Set the truck speed
        data.truck_values.current_values.dashboard_values.speed.value = self.get_float()
        data.truck_values.current_values.dashboard_values.speed.calculate_speed()

        data.truck_values.current_values.dashboard_values.rpm = self.get_float()
        data.control_values.input_values.steering = self.get_float()
        data.control_values.input_values.throttle = self.get_float()
        data.control_values.input_values.brake = self.get_float()
        data.control_values.input_values.clutch = self.get_float()
        data.control_values.game_values.steering = self.get_float()
        data.control_values.game_values.throttle = self.get_float()
        data.control_values.game_values.brake = self.get_float()
        data.control_values.game_values.clutch = self.get_float()

        # Set the cruise control speed
        data.truck_values.current_values.dashboard_values.cruise_control_speed.value = self.get_float()
        data.truck_values.current_values.dashboard_values.cruise_control_speed.calculate_speed()

        data.truck_values.current_values.motor_values.brake_values.airPressure = self.get_float()
        data.truck_values.current_values.motor_values.brake_values.temperature = self.get_float()
        data.truck_values.current_values.dashboard_values.fuel_value.amount = self.get_float()
        data.truck_values.current_values.dashboard_values.fuel_value.average_consumption = self.get_float()
        data.truck_values.current_values.dashboard_values.fuel_value.range = self.get_float()
        data.truck_values.current_values.dashboard_values.ad_blue = self.get_float()
        data.truck_values.current_values.dashboard_values.oil_pressure = self.get_float()
        data.truck_values.current_values.dashboard_values.oil_temperature = self.get_float()
        data.truck_values.current_values.dashboard_values.water_temperature = self.get_float()
        data.truck_values.current_values.dashboard_values.battery_voltage = self.get_float()
        data.truck_values.current_values.light_values.dashboard_back_light = self.get_float()
        data.truck_values.current_values.damage_values.engine = self.get_float()
        data.truck_values.current_values.damage_values.transmission = self.get_float()
        data.truck_values.current_values.damage_values.cabin = self.get_float()
        data.truck_values.current_values.damage_values.chassis = self.get_float()
        data.truck_values.current_values.damage_values.wheelsAvg = self.get_float()
        data.trailer_values.damage = self.get_float()

        data.truck_values.current_values.dashboard_values.odometer = self.get_float()
        data.navigation_values.navigation_distance = self.get_float()
        data.navigation_values.navigation_time = self.get_float()

        # Calculate the speed limit
        data.navigation_values.speed_limit.value = self.get_float()
        data.navigation_values.speed_limit.calculate_speed()

        data.trailer_values.wheel_values.susp_deflection = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.susp_deflection = self.get_float_array(self.wheel_size)
        data.trailer_values.wheel_values.velocity = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.velocity = self.get_float_array(self.wheel_size)
        data.trailer_values.wheel_values.steering = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.steering = self.get_float_array(self.wheel_size)
        data.trailer_values.wheel_values.rotation = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.rotation = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.lift = self.get_float_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.lift_offset = self.get_float_array(self.wheel_size)

        self.next_area()

    def fifth_area(self, data):
        data.truck_values.constant_values.wheel_constants.steerable = self.get_bool_array(self.wheel_size)
        data.truck_values.constant_values.wheel_constants.simulated = self.get_bool_array(self.wheel_size)
        data.truck_values.constant_values.wheel_constants.powered = self.get_bool_array(self.wheel_size)
        data.truck_values.constant_values.wheel_constants.liftable = self.get_bool_array(self.wheel_size)

        data.trailer_values.wheel_constants.steerable = self.get_bool_array(self.wheel_size)
        data.trailer_values.wheel_constants.simulated = self.get_bool_array(self.wheel_size)
        data.trailer_values.wheel_constants.powered = self.get_bool_array(self.wheel_size)
        data.trailer_values.wheel_constants.liftable = self.get_bool_array(self.wheel_size)

        data.trailer_values.attached = self.get_bool()
        data.truck_values.current_values.motor_values.brake_values.parking_brake = self.get_bool()
        data.truck_values.current_values.motor_values.brake_values.motor_brake = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.air_pressure = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.air_pressure_emergency = self.get_bool()

        data.truck_values.current_values.dashboard_values.warning_values.fuel_w = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.ad_blue = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.oil_pressure = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.water_pressure = self.get_bool()
        data.truck_values.current_values.dashboard_values.warning_values.battery_voltage = self.get_bool()
        data.truck_values.current_values.electric_enabled = self.get_bool()
        data.truck_values.current_values.engine_enabled = self.get_bool()
        data.truck_values.current_values.dashboard_values.wipers = self.get_bool()
        data.truck_values.current_values.light_values.blinker_left_active = self.get_bool()
        data.truck_values.current_values.light_values.blinker_right_active = self.get_bool()
        data.truck_values.current_values.light_values.blinker_left_on = self.get_bool()
        data.truck_values.current_values.light_values.blinker_right_on = self.get_bool()
        data.truck_values.current_values.light_values.parking = self.get_bool()
        data.truck_values.current_values.light_values.beam_low = self.get_bool()
        data.truck_values.current_values.light_values.beam_high = self.get_bool()
        data.truck_values.current_values.light_values.beacon = self.get_bool()
        data.truck_values.current_values.light_values.brake = self.get_bool()
        data.truck_values.current_values.light_values.reverse = self.get_bool()
        data.truck_values.current_values.dashboard_values.cruise_control = self.get_bool()
        data.trailer_values.wheel_values.on_ground = self.get_bool_array(self.wheel_size)
        data.truck_values.current_values.wheel_values.on_ground = self.get_bool_array(self.wheel_size)
        data.truck_values.current_values.motor_values.gear_values.h_shifter_selector = self.get_bool_array(2)

        self.next_area()

    def sixth_area(self, data):
        data.truck_values.positioning.cabin = self.get_f_vector()
        data.truck_values.positioning.head = self.get_f_vector()
        data.truck_values.positioning.hook = self.get_f_vector()
        data.truck_values.constant_values.wheel_constants.position_values = self.get_f_vector_array(self.wheel_size)
        data.trailer_values.wheel_constants.position_values = self.get_f_vector_array(self.wheel_size)

        data.trailer_values.acceleration_values.linear_velocity = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.linear_velocity = self.get_f_vector()
        data.trailer_values.acceleration_values.angular_velocity = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.angular_velocity = self.get_f_vector()
        data.trailer_values.acceleration_values.linear_acceleration = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.linear_acceleration = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.angular_acceleration = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.cabin_angular_velocity = self.get_f_vector()
        data.truck_values.current_values.acceleration_values.cabin_angular_acceleration = self.get_f_vector()

        self.next_area()

    def seventh_area(self, data):
        data.truck_values.positioning.cabin_offset = self.get_f_placement()
        data.truck_values.positioning.head_offset = self.get_f_placement()

        self.next_area()

    def eighth_area(self, data):
        position = self.get_d_placement()
        data.truck_values.current_values.position_value = position
        data.truck_values.positioning.truck_position = position
        data.trailer_values.position = self.get_d_placement()

        self.next_area()

    def ninth_area(self, data):
        data.truck_values.constant_values.brand_id = self.get_string()
        data.truck_values.constant_values.brand = self.get_string()
        data.truck_values.constant_values.id = self.get_string()
        data.trailer_values.id = self.get_string()
        data.job_values.cargo_value.accessory_id = self.get_string()
        data.truck_values.constant_values.name = self.get_string()
        data.job_values.cargo_value.id = self.get_string()
        data.job_values.cargo_value.name = self.get_string()
        data.job_values.city_destination_id = self.get_string()
        data.job_values.city_destination = self.get_string()
        data.job_values.company_destination_id = self.get_string()
        data.job_values.city_destination = self.get_string()
        data.job_values.city_source_id = self.get_string()
        data.job_values.city_source = self.get_string()
        data.job_values.company_source_id = self.get_string()
        data.job_values.company_source = self.get_string()

        shift_type = self.get_string(length=16)
        if len(shift_type) > 0:
            data.truck_values.constant_values.motor_values.shifter_type_value = SHIFTER_TYPE.index(shift_type)

        self.next_area()

    def tenth_area(self, data):
        data.job_values.income = self.get_long()

        self.next_area()

    def eleventh_area(self, data):
        data.special_events_values.on_job = self.get_bool()
        data.special_events_values.job_finished = self.get_bool()
        data.special_events_values.trailer_connected = self.get_bool()

    def set_offset(self):
        self.offset = self.offset_areas[self.offset_area]

    def next_area(self):
        self.offset_area += 1
        self.set_offset()

    def get_bool(self):
        item = self.mm[self.offset]
        self.offset += 1
        return item > 0

    def get_bool_array(self, length):
        array = []
        for _ in range(length):
            array.append(self.get_bool())
        return array

    def get_int(self):
        while self.offset % 4 != 0:
            self.offset += 1

        item = int.from_bytes(self.mm[self.offset:self.offset+4], byteorder="little", signed=True)
        self.offset += 4
        return item

    def get_int_array(self, length):
        array = []
        for _ in range(length):
            array.append(self.get_int())
        return array

    def get_uint(self):
        while self.offset % 4 != 0:
            self.offset += 1

        item = int.from_bytes(self.mm[self.offset:self.offset+4], byteorder="little", signed=False)
        self.offset += 4
        return item

    def get_uint_array(self, length):
        array = []
        for _ in range(length):
            array.append(self.get_uint())
        return array

    def get_long(self):
        item = struct.unpack('l', self.mm[self.offset:self.offset + 8])[0]
        self.offset += 8
        return item

    def get_float(self):
        while self.offset % 4 != 0:
            self.offset += 1

        item = struct.unpack('f', self.mm[self.offset:self.offset+4])[0]
        self.offset += 4
        return item

    def get_float_array(self, length):
        array = []
        for _ in range(length):
            array.append(self.get_float())
        return array

    def get_f_vector(self):
        vector = Vector(x=self.get_float(), y=self.get_float(), z=self.get_float())
        return vector

    def get_f_vector_array(self, length):
        array = []
        x_positions = self.get_float_array(length)
        y_positions = self.get_float_array(length)
        z_positions = self.get_float_array(length)
        for i in range(length):
            array.append(Vector(x_positions[i], y_positions[i], z_positions[i]))
        return array

    def get_double(self):
        while self.offset % 4 != 0:
            self.offset += 1

        item = struct.unpack('d', self.mm[self.offset:self.offset + 8])[0]
        self.offset += 8
        return item

    def get_d_vector(self):
        vector = Vector(x=self.get_double(), y=self.get_double(), z=self.get_double())
        return vector

    def get_euler(self):
        item = Euler(self.get_float(), self.get_float(), self.get_float())
        return item

    def get_d_euler(self):
        item = Euler(self.get_double(), self.get_double(), self.get_double())
        return item

    def get_f_placement(self):
        item = Placement(self.get_f_vector(), self.get_euler())
        return item

    def get_d_placement(self):
        item = Placement(self.get_d_vector(), self.get_d_euler())
        return item

    def get_string(self, length=None):
        if not length:
            length = int(self.string_size)
        item = self.mm[self.offset:self.offset+length].decode("utf-8")
        self.offset += length
        return item.replace('\x00', " ").strip()


def main():
    file_name = "Local\\SimTelemetrySCS"
    file_size = 16 * 1024
    parse_mmf = ProcessMMF(file_name, file_size)

    data = parse_mmf.parse_mmf()
    print(data)
    return 1


if __name__ == "__main__":
    exit(main())
