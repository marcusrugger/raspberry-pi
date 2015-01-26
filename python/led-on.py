#!/usr/bin/python

import RPi.GPIO
import time

CHANNEL_LED=4

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(CHANNEL_LED, RPi.GPIO.OUT)

RPi.GPIO.output(CHANNEL_LED, True)

