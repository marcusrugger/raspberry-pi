#!/usr/bin/python3

import button
import led
import camera


class CameraButton(button.Button):

    def __init__(self, channel, led):
        button.Button.__init__(self, channel)
        self.led = led
        self.camera = None


    def dispose(self):
        self.log.info('Dispose')
        if self.camera is not None : self.camera.dispose()
        if self.led    is not None : self.led.dispose()


    def action(self):
        if self.camera is None:
            self._actionCameraOn()
        else:
            self._actionCameraOff()


    def _actionCameraOn(self):
        self.log.info('Turn on camera')
        self.led.turnOn()
        self.camera = camera.Camera()
        self.camera.turnOnPreview()


    def _actionCameraOff(self):
        self.log.info('Turn off camera')
        self.led.turnOff()
        self.camera.dispose()
        self.camera = None
