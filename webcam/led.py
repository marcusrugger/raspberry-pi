#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging


class Led:
    channel=2

    def __init__(self, channel, state):
        self.logger = logging.getLogger('webcam.Led')
        self.logger.info('Instantiate LED.')

        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.set(state)

        self.logDebug(state)


    def logDebug(self, state):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('LED channel: ' + str(self.channel))
            self.logger.debug('LED state:   ' + str(state))


    def set(self, state):
        self.logger.info('Set LED state.')
        GPIO.output(self.channel, state)
        self.logDebug(state)


    def turnOn(self):
        self.logger.info('Turn on LED.')
        self.set(True)


    def turnOff(self):
        self.logger.info('Turn off LED.')
        self.set(False)
