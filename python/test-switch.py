#!/usr/bin/python

import RPi.GPIO as GPIO
import time

PIN_SWITCH=2

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SWITCH, GPIO.IN)

while True:
    if GPIO.input(PIN_SWITCH) == GPIO.LOW:
        print("Switch has been pressed")
        break

GPIO.cleanup()

