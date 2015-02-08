#!/usr/bin/python

import smbus
import time
import sys


PORT_EXPANDER   = 0x20
TEMP_SENSOR     = 0x18
HUMIDITY_SENSOR = 0x40

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

bus.write_byte_data(PORT_EXPANDER, 0x13, 0b01010101)

sensorTemperature = TemperatureSensor(bus, TEMP_SENSOR)

for loop in range(1024):
    t = sensorTemperature.read_sensor()
    sensorTemperature.print_temperature(t)

    leds = loop & 0x03
    bus.write_byte_data(PORT_EXPANDER, 0x12, leds)

    for count in range(3):
        for a in animation:
            bus.write_byte_data(PORT_EXPANDER, 0x13, a)
            time.sleep(0.1)

    for n in numbers:
        bus.write_byte_data(PORT_EXPANDER, 0x13, n)
        time.sleep(0.5)

bus.write_byte_data(PORT_EXPANDER, 0x12, 0x00)
bus.write_byte_data(PORT_EXPANDER, 0x13, 0x00)
