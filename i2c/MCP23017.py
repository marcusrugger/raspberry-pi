# Port expander


class MCP23017(object):
    BASE_ADDRESS = 0x20

    REGISTER_IODIRA = 0x00
    REGISTER_IODIRB = 0x01
    REGISTER_GPIOA  = 0x12
    REGISTER_GPIOB  = 0x13

    def __init__(self, bus, address=BASE_ADDRESS):
        self.bus = bus
        self.address = address

        self.bus.write_byte_data(self.address, self.REGISTER_IODIRA, 0x00)
        self.bus.write_byte_data(self.address, self.REGISTER_IODIRB, 0xff)

    def writePortA(self, value):
        self.bus.write_byte_data(self.address, self.REGISTER_GPIOA, value)

    def writePortB(self, value):
        self.bus.write_byte_data(self.address, self.REGISTER_GPIOB, value)
