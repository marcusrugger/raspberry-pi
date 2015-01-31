#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging


class Led:
    channel=2

    def __init__(self, channel, state):
        # 'application' code
        self.logger = logging.getLogger('webcam.led')
        self.logger.debug('debug message')

        #logging.info('%s.%s: [channel=%d]', __class__, __name__, channel)

        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.set(state)


    def set(self, state):
        GPIO.output(self.channel, state)


    def turnOn(self):
        self.set(True)


    def turnOff(self):
        self.set(False)
