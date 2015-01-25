#!/usr/bin/python

import RPi.GPIO as GPIO
import time

PIN_LED=4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LED, GPIO.OUT)

while True:
    GPIO.output(PIN_LED, True)
    time.sleep(1)
    GPIO.output(PIN_LED, False)
    time.sleep(1)

