# Python implmentation of i2c
import io
import fcntl


class Py2cBus(object):
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

        self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

        fcntl.ioctl(self.fr, I2C_SLAVE, address)
        fcntl.ioctl(self.fw, I2C_SLAVE, address)



