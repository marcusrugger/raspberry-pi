#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging


class Led:

    def __init__(self, channel, state):
        self.log = logging.getLogger('webcam.Led')
        self.log.info('Instantiate LED (channel=' + str(channel) + ').')

        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.set(state)


    def dispose(self):
        self.log.info('Dispose LED (channel=' + str(self.channel) + ').')
        self.turnOff();


    def set(self, state):
        GPIO.output(self.channel, state)


    def turnOn(self):
        self.set(True)


    def turnOff(self):
        self.set(False)
