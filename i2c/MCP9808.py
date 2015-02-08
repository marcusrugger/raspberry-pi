# Thermometer
import time


def swapBytes(value):
    lobyte      = value & 0x00ff
    hibyte      = (value & 0xff00) >> 8
    return (lobyte << 8) + hibyte


class MCP9808(object):
    BASE_ADDRESS    = 0x18

    REGISTER_AMBIENT_TEMPERATURE    = 0x05

    def __init__(self, bus, address=BASE_ADDRESS):
        self.bus = bus
        self.address = address

    def _read_sensor(self):
        return self.bus.read_word_data(self.address, MCP9808.REGISTER_AMBIENT_TEMPERATURE)

    def read_sensor(self):
        registerValue = self._read_sensor()

        # Data from sensor is in the wrong byte order, flip it around
        temp        = swapBytes(registerValue)

        whole       = (temp & 0x0ff0) >> 4
        fraction    = (temp & 0x000f)
        celsuis     = (temp & 0x0fff) / 16.0
        fahrenheit  = 1.8 * celsuis + 32.0

        # sign = sensor & 0x1000
        # if sign:
        #     whole       = -whole
        #     fahrenheit  = -fahrenheit

        rv = {}
        rv['timestamp']     = time.time()
        rv['from_chip']     = temp
        rv['whole']         = whole
        rv['fraction']      = fraction
        rv['celsuis']       = celsuis
        rv['fahrenheit']    = fahrenheit

        return rv

    def print_temperature(self, temp):
        print("Celsius: {:3} {:2}/16ths, Fahrenheit: {:4.1f}".format(temp['whole'], temp['fraction'], temp['fahrenheit']))
