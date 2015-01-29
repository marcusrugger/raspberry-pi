#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys


class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.brightness = 60

    def close(self):
        print("Closing camera.")
        self.camera.close()

    def turnOn(self):
        self.camera.start_preview()

    def turnOff(self):
        self.camera.stop_preview()
