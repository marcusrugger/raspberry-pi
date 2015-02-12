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
import logging


def setupLogging():
    loggingLevel = logging.DEBUG

    #FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    #logging.basicConfig(format=FORMAT)

    # create logger with 'spam_application'
    logger = logging.getLogger('climate_station')
    logger.setLevel(loggingLevel)

    # create file handler which logs even debug messages
    #fh = logging.FileHandler('webcam.log')
    #fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)

    # create formatter and add it to the handlers
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('[ %(levelname)5s - %(filename)16s:%(lineno)3s - %(funcName)16s ] %(message)s')
    #fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    #logger.addHandler(fh)
    logger.addHandler(ch)


setupLogging()

thermometer = TemperatureSensor(i2c(1, TemperatureSensor.BASE_ADDRESS))
hygrometer  = HumiditySensor(i2c(1, HumiditySensor.BASE_ADDRESS))
barometer   = BarometricSensor(i2c(1, BarometricSensor.BASE_ADDRESS))

poller = DevicePoller(1, thermometer, hygrometer, barometer)


ports   = PortExpander(i2c(1, PortExpander.BASE_ADDRESS))
ledbank = LedBank(ports)


display = LedDisplayController(i2c(1, LedDisplayController.BASE_ADDRESS))
display.turnOnOscillator()
display.turnOnDisplay()
display.setDimming(15)


presenter = Presenter(2, poller, ledbank, display)


print("Hello world.")

try:
    with IdleLoop() as idle:
        idle.register(poller)
        idle.register(presenter)
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    #Logger.logger.exception('Caught exception')

print("Goodbye.")
