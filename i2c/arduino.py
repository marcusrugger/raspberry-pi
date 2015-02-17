# Arduino as i2c slave
import struct
import time
import logging
from classes.logger import LogManager



class Arduino(object):
    BASE_ADDRESS = 0x77

    def __init__(self, bus):
        self.i2c = bus
        self.log = logging.getLogger('climate-station.Arduino')
        self.log.info('Arduion i2c slave.')

    def dispose(self):
        pass

    def send(self, led1, led2, led3, led4):
      try:
        with self.i2c as device:
          device.writeByteToRegister(0x00, led1)
          time.sleep(0.01)
          device.writeByteToRegister(0x01, led2)
          time.sleep(0.01)
          device.writeByteToRegister(0x02, led3)
          time.sleep(0.01)
          device.writeByteToRegister(0x03, led4)
      except OSError as e:
          self.log.error('send: Caught exception: {0}'.format(e))
