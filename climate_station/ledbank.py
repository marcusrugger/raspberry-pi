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
        try:
            value = self.ports.readPortA()
            value = (value & 0x0f) | bitmap
            self.ports.writePortA(value)
        except OSError as e:
            print('LedBank: _setLeds: Caught exception: {0}'.format(e))
            raise

    def turnOnLed1(self):
        try:
            self._setLeds(0x80)
        except OSError as e:
            print('LedBank: turnOnLed1: Caught exception: {0}'.format(e))
            raise

    def turnOnLed2(self):
        try:
            self._setLeds(0x40)
        except OSError as e:
            print('LedBank: turnOnLed2: Caught exception: {0}'.format(e))
            raise

    def turnOnLed3(self):
        try:
            self._setLeds(0x20)
        except OSError as e:
            print('LedBank: turnOnLed3: Caught exception: {0}'.format(e))
            raise

    def turnOnLed4(self):
        try:
            self._setLeds(0x10)
        except OSError as e:
            print('LedBank: turnOnLed4: Caught exception: {0}'.format(e))
            raise
