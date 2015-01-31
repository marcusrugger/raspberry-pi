#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import logging
import webcam_logger
import led
import idleloop
import toggle
import camera_button


CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

print("Hello world.")

GPIO.setmode(GPIO.BCM)

redLed = led.Led(CHANNEL_LED_RED, False)
yellowLed = led.Led(CHANNEL_LED_YELLOW, True)
toggle = toggle.Toggle(yellowLed)
cameraButton = camera_button.CameraButton(CHANNEL_SWITCH_MAIN, redLed)

try:
    with idleloop.IdleLoop() as idle:
        idle.register(toggle)
        idle.register(cameraButton)
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    webcam_logger.logger.exception('Caught exception')

print("Goodbye.")
