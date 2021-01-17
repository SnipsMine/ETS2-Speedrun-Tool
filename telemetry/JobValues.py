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

    class DeliveryTime:
        value = None

    class CargoValues:
        mass = None
        accessory_id = None
        id = None
        name = None

    class RemainingDeliveryTime:
        value = None

    def __init__(self):
        self.delivery_time = self.DeliveryTime()
        self.cargo_value = self.CargoValues()
        self.remaining_delivery_time = self.RemainingDeliveryTime()
