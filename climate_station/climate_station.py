#!/usr/bin/python

import time
import sys
from classes.idleloop import IdleLoop
from i2c.MCP9808 import MCP9808 as TemperatureSensor
from i2c.HTU21D import HTU21D as HumiditySensor
from i2c.MPL3115A2 import MPL3115A2 as BarometricSensor
from i2c.HT16K33 import HT16K33 as DisplayController
from i2c.MCP23017 import MCP23017 as PortExpander
from i2c.py2cbus import i2c


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
    h = hygrometer.read_sensor()

    display.writeTemperature(t['fahrenheit'])
    print("Temperature: [{:6.1f}, {:6.1f}], Humidity: {:5.1f}".format(t['fahrenheit'], h['fahrenheit'], h['humidity']))

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
