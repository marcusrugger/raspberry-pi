#!/usr/bin/env python

import os
import fcntl
import struct
import smbus


I2C_SLAVE=0x0703

class i2c:

   def __init__(self, bus, address):
      self.bus = bus
      self.address = address

   def __enter__(self):
      self.fd = os.open("/dev/i2c-"+str(self.bus), os.O_RDWR | os.O_SYNC)
      fcntl.ioctl(self.fd, I2C_SLAVE, self.address)
      self.smbus = smbus.SMBus(1)
      return self

   def __exit__(self, type, value, traceback):
      self.smbus.close()
      self.smbus = None
      os.close(self.fd)

   # i2c transactions
   def readByte(self):
      s = os.read(self.fd, 1)
      up, = struct.unpack("B", s)
      return up

   def readWord(self):
      return os.read(self.fd, 2)

   def readBytes(self, count):
      return os.read(self.fd, count)

   def writeByte(self, byte):
      buffer = struct.pack("B", byte)
      return os.write(self.fd, buffer)

   def writeWord(self, word):
      buffer = struct.pack("H", word)
      return os.write(self.fd, buffer)

   def writeBytes(self, bytes):
      return os.write(self.fd, bytes)

   # smbus transactions
   def readByteFromRegister(self, register):
      return self.smbus.read_byte_data(self.address, register)

   def readWordFromRegister(self, register):
      return self.smbus.read_word_data(self.address, register)

   def writeByteToRegister(self, register, byte):
      buffer = struct.pack("BB", register, byte)
      return os.write(self.fd, buffer)

   def writeWordToRegister(self, register, word):
      buffer = struct.pack("BH", register, word)
      return os.write(self.fd, buffer)

   def writeToRegister(self, register, bytes):
      buffer = struct.pack("Bs", register, bytes)
      return os.write(self.fd, buffer)


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