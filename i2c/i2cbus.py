import smbus


class I2cBus(object):
    def __init__(self, bus_number):
        self.bus = smbus.SMBus(bus_number)

    def read_byte(self, address):
        return self.bus.read_byte(address)

    def read_byte_data(self, address, register):
        return self.bus.read_byte_data(address, register)

    def read_word_data(self, address, register):
        return self.bus.read_word_data(address, register)

    def read_block_data(self, address, register):
        return self.bus.read_block_data(address, register)

    def read_i2c_block_data(self, address, register):
        return self.bus.read_i2c_block_data(address, register)

    def write_quick(self, address):
        self.bus.write_quick(address)

    def write_byte(self, address, data):
        self.bus.write_byte(address, data)

    def write_byte_data(self, address, register, data):
        self.bus.write_byte_data(address, register, data)

    def write_word_data(self, address, register, data):
        self.bus.write_word_data(address, register, data)
