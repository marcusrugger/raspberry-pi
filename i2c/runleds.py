#!/usr/bin/python

import time
import sys
from i2cbus import I2cBus
from MCP9808 import MCP9808 as TemperatureSensor
from HT16K33 import HT16K33 as DisplayController


PORT_EXPANDER   = 0x20
TEMP_SENSOR     = 0x18
HUMIDITY_SENSOR = 0x40
DISPLAY_ADDRESS = 0x70

bus = I2cBus(1)


display = DisplayController(bus, DISPLAY_ADDRESS)
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
