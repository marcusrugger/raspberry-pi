#!/usr/bin/python3

import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import sys
import logging


class Camera(PiCamera):
    _instance = None


    def instance():
        if Camera._instance is None : Camera._instance = Camera()
        return Camera._instance


    def destroy():
        if Camera._instance is not None:
            Camera._instance.dispose()
            Camera._instance = None


    def __init__(self):
        self.log = logging.getLogger('webcam.Camera')
        self.log.info('Instantiate camera.')
        PiCamera.__init__(self)
        self.configureHighRes()


    def configureLowRes(self):
        self.vflip = True
        self.hflip = True
        self.brightness = 60
        self.awb_mode = 'auto'
        self.image_effect = 'none'
        self.resolution = (640, 480)
        self.framerate = 15
        self.annotate_text = "640x480"


    def configureHighRes(self):
        self.vflip = True
        self.hflip = True
        self.brightness = 60
        self.resolution = (2592, 1944)
        self.framerate = 15
        self.annotate_text = "2592x1944"


    def configureLowResWide(self):
        self.vflip = True
        self.hflip = True
        self.brightness = 60
        self.resolution = (1296, 730)
        self.framerate = 15
        self.annotate_text = "1296x730"


    def configureHighResWide(self):
        self.vflip = True
        self.hflip = True
        self.brightness = 60
        self.resolution = (1920, 1080)
        self.framerate = 15
        self.annotate_text = "1920x1080"


    def dispose(self):
        self.log.info('Dispose camera.')
        self.close()


    def close(self):
        self.log.info('Close camera.')
        PiCamera.close(self)


    def turnOnPreview(self):
        self.log.info('Turn on camera preview.')
        self.start_preview()


    def turnOffPreview(self):
        self.log.info('Turn off camera preview.')
        self.stop_preview()
