# Arduino as i2c slave
import struct



class Arduino(object):
    BASE_ADDRESS = 0x77

    def __init__(self, bus):
        self.i2c = bus

    def dispose(self):
        pass

    def send(self, led1, led2, led3, led4):
      data = struct.pack("BBBB", led1, led2, led3, led4)
      #data = (led1 << 24) | (led2 << 16) | (led3 << 8) | led4
      #data = '\xf3'
      with self.i2c as device : device.writeBytes(data)
