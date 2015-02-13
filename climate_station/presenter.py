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
        value = self.poller.getTemperature()
        self.display.writeFixedPoint(value)
        self.ledbank.turnOnLed1()

    def modeHumidity(self):
        value = self.poller.getHumidity()
        self.display.writeFixedPoint(value)
        self.ledbank.turnOnLed2()

    def modeBarometer(self):
        value = self.poller.getPressure()
        self.display.writeFixedPoint(value)
        self.ledbank.turnOnLed3()

    def modeTime(self):
        now = datetime.now()
        t = 100 * (now.hour if now.hour <= 12 else now.hour - 12) + now.minute
        self.display.writeNumber(t)
        self.display.setColon(True)
        self.ledbank.turnOnLed4()
