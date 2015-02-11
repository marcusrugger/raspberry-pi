# Hygrometer
import time
import struct


class HTU21D(object):
    BASE_ADDRESS = 0x40

    def __init__(self, bus):
        self.i2c = bus

    def dispose(self):
        pass

    def _isValid(self, word, crc):
        return True

    def _read_measurement(self, register):
        with self.i2c as bus:
            bus.writeBytes(register)
            time.sleep(0.1)
            bytes = bus.readBytes(3)

        data = struct.unpack("3B", bytes)
        word = (data[0] << 8) + data[1]

        if not self._isValid(word, data[2]):
            raise "Checksum doesn't match"

        return word & 0xfffc

    def _read_humidity(self):
        word = self._read_measurement('\xf5')
        humidity = (-6.0) + 125.0 * word / 65536.0
        rv = {}
        rv['humidity'] = humidity
        return rv

    def _read_temperature(self):
        word = self._read_measurement('\xf3')
        celsius = (-46.85) + 175.72 * word / 65536.0
        fahrenheit = 1.8 * celsius + 32
        rv = {}
        rv['celsius']       = celsius
        rv['fahrenheit']    = fahrenheit
        return rv

    def read_sensor(self):
        h = self._read_humidity()
        t = self._read_temperature()
        return dict(h.items() + t.items())
