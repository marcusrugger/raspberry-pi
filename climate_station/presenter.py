import classes.idleloop as idleloop
from datetime import datetime


class Presenter(idleloop.Countdown):
    def __init__(self, sleep, poller, ledbank, display):
        idleloop.Countdown.__init__(self, sleep)

        self.poller     = poller
        self.ledbank    = ledbank
        self.display    = display
        self.mode       = 0

    def dispose(self):
        self.ledbank.dispose()
        self.display.dispose()

    def execute(self):
        self.mode = self.mode + 1
        if self.mode > 4 : self.mode = 1

        self.resetDisplay()
        if   self.mode is 1 : self.modeTemperature()
        elif self.mode is 2 : self.modeHumidity()
        elif self.mode is 3 : self.modeBarometer()
        elif self.mode is 4 : self.modeTime()

    def resetDisplay(self):
        self.display.setColon(False)

    def modeTemperature(self):
        try:
            value = self.poller.get_readings()["temperature"]["farhenheit"]
            self.display.writeFixedPoint(value)
            self.ledbank.turnOnLed1()
        except OSError as e:
            print('Presenter: modeTemperature: Caught exception: {0}'.format(e))
            raise

    def modeHumidity(self):
        try:
            value = self.poller.get_readings()["humidity"]["relative"]
            self.display.writeFixedPoint(value)
            self.ledbank.turnOnLed2()
        except OSError as e:
            print('Presenter: modeHumidity: Caught exception: {0}'.format(e))
            raise

    def modeBarometer(self):
        try:
            value = self.poller.get_readings()["pressure"]["inHg"]
            self.display.writeFixedPoint(value)
            self.ledbank.turnOnLed3()
        except OSError as e:
            print('Presenter: modeBarometer: Caught exception: {0}'.format(e))
            raise

    def modeTime(self):
        try:
            now = datetime.now()
            t = 100 * (now.hour if now.hour <= 12 else now.hour - 12) + now.minute
            self.display.writeNumber(t)
            self.display.setColon(True)
            self.ledbank.turnOnLed4()
        except OSError as e:
            print('Presenter: modeTime: Caught exception: {0}'.format(e))
            raise
