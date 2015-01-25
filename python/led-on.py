#!/usr/bin/python

import RPi.GPIO
import time

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(2, RPi.GPIO.OUT)

RPi.GPIO.output(2, True)

