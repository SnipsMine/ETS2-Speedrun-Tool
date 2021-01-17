from mmap import mmap
from telemetry import Telemetry


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
        pass

    def set_offset(self):
        self.offset = self.offset_areas[self.offset_area]

    def get_bool(self):
        item = self.mm[self.offset]
        self.offset += 1
        return item




def main():
    file_name = "Local\\SimTelemetrySCS"
    file_size = 16 * 1024
    parse_mmf = ProcessMMF(file_name, file_size)

    parse_mmf.read_mmf()

    return 1


if __name__ == "__main__":
    exit(main())
