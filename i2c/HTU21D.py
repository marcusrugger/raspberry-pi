# Hygrometer
import time
from i2cdevice import I2cDevice


class HTU21D(I2cDevice):
    BASE_ADDRESS = 0x40

    def __init__(self, bus, address=BASE_ADDRESS):
        I2cDevice.__init__(self, bus, address)

    def read_humidity(self):
        I2cDevice.write_byte(self, 0xf5)
        print("humidity: write successful")
        time.sleep(1)
        b1 = I2cDevice.read_byte(self)
        print("humidity: 0x{:x}".format(b1))
        b2 = I2cDevice.read_byte(self)
        print("humidity: 0x{:2x}, 0x{:2x}".format(b1, b2))
        b3 = I2cDevice.read_byte(self)
        print("humidity: 0x{:2x}, 0x{:2x}, 0x{:2x}".format(b1, b2, b3))
