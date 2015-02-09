

class I2cDevice(object):
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read_byte_data(self, register):
        return self.bus.read_byte_data(self.address, register)

    def read_word_data(self, register):
        return self.bus.read_word_data(self.address, register)

    def read_block_data(self, register):
        return self.bus.read_block_data(self.address, register)

    def write_byte_data(self, register, data=None):
        self.bus.write_byte_data(self.address, register, data)

    def write_word_data(self, register, data=None):
        self.bus.write_word_data(self.address, register, data)
