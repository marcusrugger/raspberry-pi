import classes.idleloop as idleloop


class Presenter(idleloop.Countdown):
    def __init__(self, sleep, poller, ledbank, display):
        idleloop.Countdown.__init__(self, sleep)

        self.poller     = poller
        self.ledbank    = ledbank
        self.display    = display
        self.mode       = 0

    def dispose(self):
        self.ledbank.dispose()

    def execute(self):
        self.mode = self.mode + 1
        if self.mode > 4 : self.mode = 1

        if   self.mode is 1 : self.modeTemperature()
        elif self.mode is 2 : self.modeHumidity()
        elif self.mode is 3 : self.modeBarometer()
        elif self.mode is 4 : self.modeTime()

    def modeTemperature(self):
        value = self.poller().temperature()
        self.display.writeFixedPoint(value)
        self.ledbank.turnOnLed1()

    def modeHumidity(self):
        value = self.poller().humidity()
        self.display.writeFixedPoint(t)
        self.ledbank.turnOnLed2()

    def modeBarometer(self):
        value = self.poller().pressure()
        self.display.writeFixedPoint(t)
        self.ledbank.turnOnLed3()

    def modeTime(self):
        self.ledbank.turnOnLed4()
