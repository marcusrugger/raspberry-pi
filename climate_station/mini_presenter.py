import classes.idleloop as idleloop
from datetime import datetime
import RPi.GPIO as GPIO


class QuickPresenter(idleloop.Countdown):
    PIN_SWITCH=22

    DISPLAY_MODE_OFF            = 0
    DISPLAY_MODE_TEMPERATURE    = (DISPLAY_MODE_OFF + 1)
    DISPLAY_MODE_HUMIDITY       = (DISPLAY_MODE_TEMPERATURE + 1)
    DISPLAY_MODE_ENDOF          = (DISPLAY_MODE_HUMIDITY + 1)

    def __init__(self, sleep, poller, display):
        idleloop.Countdown.__init__(self, sleep)

        self.poller         = poller
        self.display        = display
        self.mode           = 0
        self.isDisplayOn    = False
        self.display_mode   = QuickPresenter.DISPLAY_MODE_OFF

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(QuickPresenter.PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def dispose(self):
        self.display.dispose()

    def execute(self):
        mode = self.displayMode()
        if mode == QuickPresenter.DISPLAY_MODE_OFF:
            self.turnOffDisplay()
        elif mode == QuickPresenter.DISPLAY_MODE_TEMPERATURE:
            self.modeTemperature()
        elif mode == QuickPresenter.DISPLAY_MODE_HUMIDITY:
            self.modeHumidity()

    def displayMode(self):
        isButtonPressed = GPIO.input(self.PIN_SWITCH) == GPIO.LOW
        if isButtonPressed : self.bumpDisplayMode()
        return self.display_mode

    def bumpDisplayMode(self):
        self.display_mode = self.display_mode + 1
        if self.display_mode >= QuickPresenter.DISPLAY_MODE_ENDOF : self.display_mode = self.DISPLAY_MODE_OFF

    def turnOnDisplay(self):
        if not self.isDisplayOn:
            self.display.turnOnOscillator()
            self.display.turnOnDisplay()
            self.isDisplayOn = True

    def turnOffDisplay(self):
        if self.isDisplayOn:
            self.display.turnOffDisplay()
            self.display.turnOffOscillator()
            self.isDisplayOn = False

    def resetDisplay(self):
        self.display.setColon(False)

    def modeTemperature(self):
        try:
            self.turnOnDisplay()
            reading = self.poller.get_readings()
            value = reading["sensor"]["temperature"]["fahrenheit"]
            self.display.writeFixedPoint(value)
        except OSError as e:
            print('Presenter: modeTemperature: Caught exception: {0}'.format(e))
            raise

    def modeHumidity(self):
        try:
            self.turnOnDisplay()
            reading = self.poller.get_readings()
            value = reading["sensor"]["humidity"]["relative"]
            self.display.writeFixedPoint(value)
        except OSError as e:
            print('Presenter: modeHumidity: Caught exception: {0}'.format(e))
            raise
