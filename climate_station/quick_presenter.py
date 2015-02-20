import classes.idleloop as idleloop
from datetime import datetime
import RPi.GPIO as GPIO


class QuickPresenter(idleloop.Countdown):
    PIN_SWITCH=22

    def __init__(self, sleep, poller, display):
        idleloop.Countdown.__init__(self, sleep)

        self.poller         = poller
        self.display        = display
        self.mode           = 0
        self.isDisplayOn    = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(QuickPresenter.PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def dispose(self):
        self.display.dispose()

    def execute(self):
        if self.isDisplayed():
            self.turnOnDisplay()
            self.mode = self.mode + 1
            if self.mode > 2 : self.mode = 1

            self.resetDisplay()
            if   self.mode is 1 : self.modeTemperature()
            elif self.mode is 2 : self.modeHumidity()
        else:
            self.turnOffDisplay()

    def isDisplayed(self):
        return GPIO.input(self.PIN_SWITCH) == GPIO.LOW

    def turnOnDisplay(self):
        if not self.isDisplayOn:
            self.display.turnOnOscillator()
            self.display.turnOnDisplay()
            self.isDisplayOn = True

    def turnOffDisplay(self):
        if self.isDisplayOn:
            self.display.turnOffOscillator()
            self.display.turnOffDisplay()
            self.isDisplayOn = False

    def resetDisplay(self):
        self.display.setColon(False)

    def modeTemperature(self):
        try:
            reading = self.poller.get_readings()
            print(reading)
            print(reading["sensor"])
            print(reading["sensor"]["temperature"])
            value = reading["sensor"]["temperature"]["fahrenheit"]
            self.display.writeFixedPoint(value)
        except OSError as e:
            print('Presenter: modeTemperature: Caught exception: {0}'.format(e))
            raise

    def modeHumidity(self):
        try:
            value = self.poller.get_readings()["sensor"]["humidity"]["relative"]
            self.display.writeFixedPoint(value)
        except OSError as e:
            print('Presenter: modeHumidity: Caught exception: {0}'.format(e))
            raise
