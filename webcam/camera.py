#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys
import logging


class Camera:
    def __init__(self):
        self.logger = logging.getLogger('webcam.Camera')
        self.logger.info('Instantiate camera.')
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.brightness = 60

    def close(self):
        self.logger.info('Close camera.')
        self.camera.close()

    def turnOnPreview(self):
        self.logger.info('Turn on camera preview.')
        self.camera.start_preview()

    def turnOffPreview(self):
        self.logger.info('Turn off camera preview.')
        self.camera.stop_preview()
