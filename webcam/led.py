#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys


class Led:
    channel=2
    state=False

    def __init__(self, channel, state):
        self.channel = channel
        self.state = state
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, self.state)

    def set(self, state):
        self.state = state
        GPIO.output(self.channel, self.state)


    def toggleState(self):
        self.set(not self.state)

    def turnOn(self):
        self.set(True)

    def turnOff(self):
        self.set(False)
