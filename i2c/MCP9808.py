# Thermometer
import time
from datetime import datetime


def swapBytes(word):
    return ((word & 0x00ff) << 8) + ((word & 0xff00) >> 8)


class MCP9808(object):
    BASE_ADDRESS    = 0x18

    REGISTER_AMBIENT_TEMPERATURE    = 0x05

    def __init__(self, bus):
        self.i2c = bus

    def dispose(self):
        pass

    def _read_sensor(self):
        with self.i2c as bus : rv = bus.readWordFromRegister(MCP9808.REGISTER_AMBIENT_TEMPERATURE)
        return rv

    def read_sensor(self):
        register    = self._read_sensor()

        # Data from sensor is in the wrong byte order, swap 'em
        register    = swapBytes(register)
        sign        = -1 if register & 0x1000 > 0 else 1

        whole       = sign * ((register & 0x0ff0) >> 4)
        fraction    = (register & 0x000f)
        celsius     = sign * (register & 0x0fff) / 16.0
        fahrenheit  = 1.8 * celsius + 32.0

        t = {}
        t['register']       = hex(register)
        t['celsius']        = int(10 * celsius + 0.5) / 10.0
        t['fahrenheit']     = int(10 * fahrenheit + 0.5) / 10.0

        rv = {}
        rv['timestamp']     = datetime.now().isoformat()
        rv['temperature']   = t

        return rv
