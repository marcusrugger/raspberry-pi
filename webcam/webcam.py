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

redLed = led.Led(CHANNEL_LED_RED, True)
camera = camera.Camera()
camera.turnOn()

idle = idleloop.IdleLoop()
toggle = toggle.Toggle(redLed)
idle.register(toggle)

try:
    idle.run()

except:
    e = sys.exc_info()[0]
    print('Caught exception: {0}'.format(e))
    pass


camera.turnOff()
camera.close()
redLed.turnOff()

print("Goodbye.")
