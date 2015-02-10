#!/usr/bin/python

import time
import sys
from classes.idleloop import IdleLoop
from MCP9808 import MCP9808 as TemperatureSensor
from HTU21D import HTU21D as HumiditySensor
from MPL3115A2 import MPL3115A2 as BarometricSensor
from HT16K33 import HT16K33 as DisplayController
from MCP23017 import MCP23017 as PortExpander
from py2cbus import i2c


thermometer = TemperatureSensor(i2c(1, TemperatureSensor.BASE_ADDRESS))
hygrometer  = HumiditySensor(i2c(1, HumiditySensor.BASE_ADDRESS))
barometer   = BarometricSensor(i2c(1, BarometricSensor.BASE_ADDRESS))


ports = PortExpander(i2c(1, PortExpander.BASE_ADDRESS))
ports.writePortA(0x00)

display = DisplayController(i2c(1, DisplayController.BASE_ADDRESS))
display.turnOnOscillator()
display.turnOnDisplay()
display.setDimming(0)

for loop in range(1024):
    t = thermometer.read_sensor()
    thermometer.print_temperature(t)
    display.writeTemperature(t['fahrenheit'])

    h = hygrometer.read_sensor()
    print("Humidity: {:5.1f}, Temperature: {:6.1f}".format(h['humidity'], h['fahrenheit']))

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
