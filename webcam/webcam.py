#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import logging
import webcam_logger as Logger
from idleloop import IdleLoop
from led import Led
from toggle_led import ToggleLed
from camera_button import CameraButton as CameraButton


CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

print("Hello world.")

GPIO.setmode(GPIO.BCM)

redLed = Led(CHANNEL_LED_RED, False)
yellowLed = ToggleLed(1, CHANNEL_LED_YELLOW, True)

try:
    with IdleLoop() as idle:
        idle.register(yellowLed)
        idle.register(CameraButton(CHANNEL_SWITCH_MAIN, redLed))
        idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    Logger.logger.exception('Caught exception')

print("Goodbye.")
