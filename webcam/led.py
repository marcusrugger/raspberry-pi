#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys


class Led:
    channel=2

    def __init__(self, channel, state):
        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.set(state)


    def set(self, state):
        GPIO.output(self.channel, state)


    def turnOn(self):
        self.set(True)


    def turnOff(self):
        self.set(False)
