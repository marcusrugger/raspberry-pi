#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys
import logging


class Camera:
    def __init__(self):
        self.log = logging.getLogger('webcam.Camera')
        self.log.info('Instantiate camera.')
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.brightness = 60

    def close(self):
        self.log.info('Close camera.')
        self.camera.close()

    def turnOnPreview(self):
        self.log.info('Turn on camera preview.')
        self.camera.start_preview()

    def turnOffPreview(self):
        self.log.info('Turn off camera preview.')
        self.camera.stop_preview()
