#!/usr/bin/python

import time
import sys
import logging
from classes.idleloop import IdleLoop
from i2c.HTU21D import HTU21D as Sensor
from i2c.HT16K33 import HT16K33 as LedDisplayController
from i2c.py2cbus import i2c
from device_poller import DevicePoller
from mini_presenter import QuickPresenter as Presenter
from classes.logger import LogManager
from data_logger import DataLogger


LogManager.setupLogging("climate-station")
log = logging.getLogger('climate-station')
log.info('Hello world.')

sensor  = Sensor(i2c(1, Sensor.BASE_ADDRESS))

poller = DevicePoller(1)
poller.add_device("sensor", sensor)

display = LedDisplayController(i2c(1, LedDisplayController.BASE_ADDRESS))
display.turnOnOscillator()
display.turnOnDisplay()
display.setDimming(0)


presenter = Presenter(2, poller, display)


dataLogger = DataLogger(60, poller)


try:
    with IdleLoop() as idle:
        idle.setTicksPerSecond(1)
        idle.register(dataLogger)
        idle.register(presenter)
        idle.run()

except:
    e = sys.exc_info()[0]
    log.exception(e)
    print('Caught exception: {0}'.format(e))
