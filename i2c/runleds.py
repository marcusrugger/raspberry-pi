#!/usr/bin/python

import smbus
import time
import sys


PORT_EXPANDER   = 0x20
TEMP_SENSOR     = 0x18
HUMIDITY_SENSOR = 0x40
DISPLAY_ADDRESS = 0x70

bus             = smbus.SMBus(1)


class TemperatureSensor:
    REGISTER_AMBIENT_TEMPERATURE    = 0x05

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read_sensor(self):
        rv = {}

        temp        = self.bus.read_word_data(self.address, TemperatureSensor.REGISTER_AMBIENT_TEMPERATURE)
        lobyte      = temp & 0x00ff
        hibyte      = (temp & 0xff00) >> 8
        temp        = (lobyte << 8) + hibyte
        whole       = (temp & 0x0ff0) >> 4
        fraction    = (temp & 0x000f)
        fahrenheit  = ((temp & 0x0fff) / 16.0) * 1.8 + 32.0

        rv['from_chip']     = temp
        rv['whole']         = whole
        rv['fraction']      = fraction
        rv['fahrenheit']    = fahrenheit

        return rv

    def print_temperature(self, temp):
        print("Celsius: {:3} {:2}/16ths, Fahrenheit: {:4.1f}".format(temp['whole'], temp['fraction'], temp['fahrenheit']))


class Display:
    POSITION1 = 0x00
    POSITION2 = 0x02
    POSITION3 = 0x06
    POSITION4 = 0x08

    character_set = [   0x3f,   # 0
                        0x06,   # 1
                        0x5b,   # 2
                        0x4f,   # 3
                        0x66,   # 4
                        0x6d,   # 5
                        0x7d,   # 6
                        0x07,   # 7
                        0x7f,   # 8
                        0x6f    # 9
                    ]

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.bus.write_byte_data(self.address, 0x21, 0x00)
        self.bus.write_byte_data(self.address, 0x00, 0x7f)
        self.bus.write_byte_data(self.address, 0x02, 0x7f)
        self.bus.write_byte_data(self.address, 0x04, 0x00)
        self.bus.write_byte_data(self.address, 0x06, 0x7f)
        self.bus.write_byte_data(self.address, 0x08, 0x7f)

    def turnOnDisplay(self):
        self.bus.write_byte_data(self.address, 0x81, 0x00)

    def turnOffDisplay(self):
        self.bus.write_byte_data(self.address, 0x80, 0x00)

    def setDimming(self, dim):
        if dim < 0:
            dim = 0
        elif dim > 15:
            dim = 15
        self.bus.write_byte_data(self.address, 0xe0 | dim, 0x00)

    def writeNumber(self, number):
        d4 = number % 10

        number = int(number/10)
        d3 = number % 10

        number = int(number/10)
        d2 = number % 10

        number = int(number/10)
        d1 = number % 10

        self._writeDigit(Display.POSITION1, d1)
        self._writeDigit(Display.POSITION2, d2)
        self._writeDigit(Display.POSITION3, d3)
        self._writeDigit(Display.POSITION4, d4)

    def writeTemperature(self, temp):
        number = int(10 * temp)
        d4 = number % 10

        number = int(number/10)
        d3 = number % 10

        number = int(number/10)
        d2 = number % 10

        number = int(number/10)
        d1 = number % 10

        if d1 > 0:
            self._writeDigit(Display.POSITION1, d1)
        else:
            self.bus.write_byte_data(self.address, Display.POSITION1, 0x00)

        if d1 > 0 or d2 > 0:
            self._writeDigit(Display.POSITION2, d2)
        else:
            self.bus.write_byte_data(self.address, Display.POSITION2, 0x00)

        self._writeDigit(Display.POSITION3, d3, True)
        self._writeDigit(Display.POSITION4, d4)

    def _writeDigit(self, position, number, isDot=False):
        bitmap = Display.character_set[number]
        if isDot : bitmap = bitmap | 0x80
        self.bus.write_byte_data(self.address, position, bitmap)


display = Display(bus, DISPLAY_ADDRESS)
display.turnOnDisplay()
display.setDimming(0)

#for a in range(10000) : display.writeNumber(a)


bus.write_byte_data(PORT_EXPANDER, 0x00, 0x00)
bus.write_byte_data(PORT_EXPANDER, 0x01, 0x00)

animation = [   0b00000001,
                0b01000000,
                0b00001000,
                0b00000100,
                0b00000010,
                0b01000000,
                0b00010000,
                0b00100000 ]

numbers = [ 0b00111111,
            0b00011000,
            0b01101101,
            0b01111100,
            0b01011010,
            0b01110110,
            0b01110111,
            0b00011100,
            0b01111111,
            0b01111110 ]

sensorTemperature = TemperatureSensor(bus, TEMP_SENSOR)

for loop in range(1024):
    t = sensorTemperature.read_sensor()
    sensorTemperature.print_temperature(t)
    display.writeTemperature(t['fahrenheit'])
    time.sleep(60)

bus.write_byte_data(PORT_EXPANDER, 0x12, 0x00)
bus.write_byte_data(PORT_EXPANDER, 0x13, 0x00)
