#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import camera
import led

CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

print("Hello world.")

GPIO.setmode(GPIO.BCM)

redLed = led.Led(CHANNEL_LED_RED, True)
camera = camera.Camera()
camera.turnOn()

time.sleep(5)

camera.turnOff()
camera.close()
redLed.turnOff()

print("Goodbye.")
