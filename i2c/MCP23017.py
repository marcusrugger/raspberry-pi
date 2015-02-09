# Port expander
from i2cdevice import I2cDevice


class MCP23017(I2cDevice):
    BASE_ADDRESS = 0x20

    REGISTER_IODIRA = 0x00
    REGISTER_IODIRB = 0x01
    REGISTER_GPPUA  = 0x0c
    REGISTER_GPPUB  = 0x0d
    REGISTER_GPIOA  = 0x12
    REGISTER_GPIOB  = 0x13

    def __init__(self, bus, address=BASE_ADDRESS):
        I2cDevice.__init__(self, bus, address)

        I2cDevice.write_byte_data(self, MCP23017.REGISTER_IODIRA, 0x00)
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_IODIRB, 0xff)
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_GPPUB, 0xff)

        gppua = I2cDevice.read_byte_data(self, MCP23017.REGISTER_GPPUA)
        gppub = I2cDevice.read_byte_data(self, MCP23017.REGISTER_GPPUB)

        print("gppub = 0x{:2x}".format(gppub))

    def dispose(self):
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_IODIRA, 0xff)
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_IODIRB, 0xff)

    def writePortA(self, value):
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_GPIOA, value)

    def writePortB(self, value):
        I2cDevice.write_byte_data(self, MCP23017.REGISTER_GPIOB, value)

    def readPortA(self):
        return I2cDevice.read_byte_data(self, MCP23017.REGISTER_GPIOA) ^ 0xff

    def readPortB(self):
        return I2cDevice.read_byte_data(self, MCP23017.REGISTER_GPIOB) ^ 0xff
