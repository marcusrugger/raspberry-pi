#!/usr/bin/env python

import os
import fcntl

I2C_SLAVE=0x0703

class i2c:

   def __init__(self, bus, address):
      self.bus = bus
      self.address = address

   def __enter__(self):
      self.fd = os.open("/dev/i2c-"+str(self.bus), O_RDWR | O_SYNC)
      fcntl.ioctl(self.fd, I2C_SLAVE, self.address)
      return self

   def __exit__(self, type, value, traceback):
      os.close(self.fd)

   def readByte():
      return os.read(self.fd, 1)

   def readWord():
      return os.read(self.fd, 2)

   def readBytes(count):
      return os.read(self.fd. count)

   def writeBytes(bytes):
      os.write(self.fd, bytes)


# if __name__ == "__main__":

#    import time
#    import struct

#    import i2c

#    dev = i2c.i2c(0x53, 1) # device 0x53, bus 1

#    dev.write("\x2D\x00") # POWER_CTL reset
#    dev.write("\x2D\x08") # POWER_CTL measure
#    dev.write("\x31\x00") # DATA_FORMAT reset
#    dev.write("\x31\x0B") # DATA_FORMAT full res +/- 16g

#    num_samples=5000

#    sample=[(0,0,0)]*num_samples

#    start1 = time.time()

#    for s in xrange(num_samples):

#       dev.write("\x32")
#       sample[s] = struct.unpack('3h', dev.read(6))
#       print("x={} y={} z={}".format(sample[s][0], sample[s][1], sample[s][2]))

#    end1 = time.time()

#    print(end1-start1)

#    dev.close()