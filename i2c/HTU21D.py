# Hygrometer


class HTU21D(object):
    BASE_ADDRESS = 0x40

    def __init__(self, bus, address=BASE_ADDRESS):
        self.bus = bus
        self.address = address
