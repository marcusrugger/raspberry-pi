# Barometer/Altimeter


class MPL3115A2(object):
    BASE_ADDRESS = 0x60

    def __init__(self, bus):
        self.i2c = bus
