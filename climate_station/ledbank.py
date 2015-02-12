# led bank
import logging


class LedBank(object):
    def __init__(self, ports):
        self.ports = ports
        self._setLeds(0x00)
        self.log = logging.getLogger('webcam.LedBank')
        self.log.info('Instantiate LED bank.')

    def dispose(self):
        self.log.debug('Dispose LedBank.')
        self._setLeds(0x00)

    def _setLeds(self, bitmap):
        value = self.ports.readPortA()
        value = (value & 0x0f) | bitmap
        self.ports.writePortA(value)

    def turnOnLed1(self):
        self._setLeds(0x80)

    def turnOnLed2(self):
        self._setLeds(0x40)

    def turnOnLed3(self):
        self._setLeds(0x20)

    def turnOnLed4(self):
        self._setLeds(0x10)
