# Barometer/Altimeter
from i2cdevice import I2cDevice


class MPL3115A2(I2cDevice):
    BASE_ADDRESS = 0x60

    def __init__(self, bus, address=BASE_ADDRESS):
        I2cDevice.__init__(self, bus, address)
