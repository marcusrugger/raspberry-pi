#!/usr/bin/python

import time
import sys
from i2cbus import I2cBus
from MCP9808 import MCP9808 as TemperatureSensor
from HTU21D import HTU21D as HumiditySensor
from MPL3115A2 import MPL3115A2 as BarometricSensor
from HT16K33 import HT16K33 as DisplayController
from MCP23017 import MCP23017 as PortExpander


bus = I2cBus(1)

thermometer = TemperatureSensor(bus)
hygrometer  = HumiditySensor(bus)
barometer   = BarometricSensor(bus)

ports = PortExpander(bus)
ports.writePortA(0x00)

display = DisplayController(bus)
display.turnOnOscillator()
display.turnOnDisplay()
display.setDimming(0)

for loop in range(1024):
    t = thermometer.read_sensor()
    thermometer.print_temperature(t)
    display.writeTemperature(t['fahrenheit'])
    time.sleep(60)
