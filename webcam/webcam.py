#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import camera
import webcam_logger
import led
import idleloop
import toggle



CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

print("Hello world.")

GPIO.setmode(GPIO.BCM)

redLed = led.Led(CHANNEL_LED_RED, False)
yellowLed = led.Led(CHANNEL_LED_YELLOW, True)
toggle = toggle.Toggle(yellowLed)

try:
    with idleloop.IdleLoop() as idle:
        idle.register(toggle)
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))

print("Goodbye.")
