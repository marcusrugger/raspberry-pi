#!/usr/bin/python3

from button import Button
from camera import Camera


class CameraButton(Button):

    def __init__(self, channel, led):
        Button.__init__(self, channel)
        self.isCameraOn = False
        self.led = led


    def dispose(self):
        self.log.info('Dispose')
        Camera.destroy()
        if self.led    is not None : self.led.dispose()


    def actionPressed(self):
        self.isCameraOn = not self.isCameraOn
        if self.isCameraOn:
            self._actionTurnOnCamera()
        else:
            self._actionTurnOffCamera()


    def _actionTurnOnCamera(self):
        self.log.info('Turn on camera')
        self.led.turnOn()
        Camera.instance().turnOnPreview()


    def _actionTurnOffCamera(self):
        self.log.info('Turn off camera')
        self.led.turnOff()
        Camera.destroy()



class CameraButtonMode(Button):

    def __init__(self, channel, led):
        Button.__init__(self, channel)
        self.led = led
        self.camera = Camera()
        self.camera.led = False
        self.toggle = True
        self.led.turnOn()
        self._actionMode2()


    def dispose(self):
        self.log.info('Dispose')
        if self.camera is not None : self.camera.dispose()
        if self.led    is not None : self.led.dispose()


    def actionPressed(self):
        self.toggle = not self.toggle
        if self.toggle:
            self._actionMode1()
        else:
            self._actionMode2()


    def _actionMode1(self):
        self.log.info('Set camera to mode 1')
        self.camera.turnOffPreview()
        self.camera.configureHighRes()
        self.camera.turnOnPreview()


    def _actionMode2(self):
        self.log.info('Set camera to mode 2')
        self.camera.turnOffPreview()
        self.camera.configureLowRes()
        self.camera.turnOnPreview()
