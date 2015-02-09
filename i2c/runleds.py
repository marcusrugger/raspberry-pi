#!/usr/bin/python

import time
import sys
from classes.idleloop import IdleLoop
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
    for sleep in range(600):
        portb = ports.readPortB()
        if (portb & 0x0f) > 0 : print("Button pressed!: 0x{:2x}".format(portb))
        time.sleep(0.1)

print("Hello world.")

try:
    with IdleLoop() as idle:
        #idle.register(ToggleLed(1, CHANNEL_LED_YELLOW, True))
        #idle.register(CameraButton(CHANNEL_SWITCH_MAIN, Led(CHANNEL_LED_RED, False)))
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    Logger.logger.exception('Caught exception')

print("Goodbye.")
