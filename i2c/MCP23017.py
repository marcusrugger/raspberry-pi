# Port expander



class MCP23017(object):
    BASE_ADDRESS = 0x20

    REGISTER_IODIRA = 0x00
    REGISTER_IODIRB = 0x01
    REGISTER_GPPUA  = 0x0c
    REGISTER_GPPUB  = 0x0d
    REGISTER_GPIOA  = 0x12
    REGISTER_GPIOB  = 0x13

    def __init__(self, bus):
        self.i2c = bus

        with self.i2c as bus:
            bus.writeByteToRegister(MCP23017.REGISTER_IODIRA, 0x00)
            bus.writeByteToRegister(MCP23017.REGISTER_IODIRB, 0xff)
            bus.writeByteToRegister(MCP23017.REGISTER_GPPUB,  0xff)

            gppua = bus.readByteFromRegister(MCP23017.REGISTER_GPPUA)
            gppub = bus.readByteFromRegister(MCP23017.REGISTER_GPPUB)

    def dispose(self):
        with self.i2c as bus:
            bus.writeByteToRegister(MCP23017.REGISTER_IODIRA, 0xff)
            bus.writeByteToRegister(MCP23017.REGISTER_IODIRB, 0xff)

    def writePortA(self, value):
        with self.i2c as bus:
            bus.writeByteToRegister(MCP23017.REGISTER_GPIOA, value)

    def writePortB(self, value):
        with self.i2c as bus:
            bus.writeByteToRegister(MCP23017.REGISTER_GPIOB, value)

    def readPortA(self):
        with self.i2c as bus:
            return bus.readByteFromRegister(MCP23017.REGISTER_GPIOA) ^ 0xff

    def readPortB(self):
        with self.i2c as bus:
            return bus.readByteFromRegister(MCP23017.REGISTER_GPIOB) ^ 0xff
