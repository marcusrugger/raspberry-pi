# Barometer/Altimeter


class MPL3115A2(object):
    BASE_ADDRESS = 0x60

    def __init__(self, bus):
        self.i2c = bus

    def dispose(self):
        pass

    def read_sensor():
        return { "pressure": 0.0 }
