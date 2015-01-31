#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging


class Led:
    channel=2

    def __init__(self, channel, state):
        self.log = logging.getLogger('webcam.Led')
        self.log.info('Instantiate LED (channel=' + str(channel) + ').')

        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.set(state)

        self.logDebug('__init__', state)


    def dispose(self):
        self.log.info('Dispose LED (channel=' + str(self.channel) + ').')
        self.turnOff();


    def logDebug(self, description, state):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug(description)
            self.log.debug('  LED channel: ' + str(self.channel))
            self.log.debug('  LED state:   ' + str(state))


    def set(self, state):
        GPIO.output(self.channel, state)
        self.logDebug('Set state', state)


    def turnOn(self):
        self.log.info('Turn on LED.')
        self.set(True)


    def turnOff(self):
        self.log.info('Turn off LED.')
        self.set(False)
