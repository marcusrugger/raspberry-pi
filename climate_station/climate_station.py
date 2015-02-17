#!/usr/bin/python

import time
import sys
from classes.idleloop import IdleLoop
from i2c.MCP9808 import MCP9808 as TemperatureSensor
from i2c.HTU21D import HTU21D as HumiditySensor
from i2c.MPL3115A2 import MPL3115A2 as BarometricSensor
from i2c.HT16K33 import HT16K33 as LedDisplayController
from i2c.MCP23017 import MCP23017 as PortExpander
from i2c.py2cbus import i2c
from device_poller import DevicePoller
from ledbank import LedBank
from presenter import Presenter
from i2c.arduino import Arduino
from classes.logger import LogManager
from data_logger import DataLogger

print("Hello world.")


LogManager.setupLogging("climate-station")

thermometer = TemperatureSensor(i2c(1, TemperatureSensor.BASE_ADDRESS))
hygrometer  = HumiditySensor(i2c(1, HumiditySensor.BASE_ADDRESS))
barometer   = BarometricSensor(i2c(1, BarometricSensor.BASE_ADDRESS))

poller = DevicePoller(1, thermometer, hygrometer, barometer)


ports   = PortExpander(i2c(1, PortExpander.BASE_ADDRESS))
arduino = Arduino(i2c(1, Arduino.BASE_ADDRESS))
ledbank = LedBank(ports, arduino)


display = LedDisplayController(i2c(1, LedDisplayController.BASE_ADDRESS))
display.turnOnOscillator()
display.turnOnDisplay()
display.setDimming(15)


presenter = Presenter(2, poller, ledbank, display)


dataLogger = DataLogger(60, poller)


try:
    with IdleLoop() as idle:
        idle.register(dataLogger)
        idle.register(presenter)
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    #Logger.logger.exception('Caught exception')

print("Goodbye.")
