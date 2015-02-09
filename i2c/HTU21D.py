# Hygrometer
from i2cdevice import I2cDevice


class HTU21D(I2cDevice):
    BASE_ADDRESS = 0x40

    def __init__(self, bus, address=BASE_ADDRESS):
        I2cDevice.__init__(self, bus, address)

    def read_humidity(self):
        rv = I2cDevice.read_block_data(self, 0xe5)
        print("humidity: {}".format(rv))
