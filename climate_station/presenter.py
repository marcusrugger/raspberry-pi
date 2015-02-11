import classes.idleloop as idleloop


class Presenter(idleloop.Countdown):
    def __init__(self, sleep, poller, ledbank):
        idleloop.Countdown.__init__(self, sleep)

        self.poller     = poller
        self.ledbank    = ledbank
        self.mode       = 1

    def dispose(self):
        self.ledbank.dispose()

    def execute(self):
        if self.mode is 1:
            self.mode = self.mode1()
        elif self.mode is 2:
            self.mode = self.mode2()
        elif self.mode is 3:
            self.mode = self.mode3()
        elif self.mode is 4:
            self.mode = self.mode4()

    def mode1(self):
        self.ledbank.turnOnLed1()
        return 2

    def mode2(self):
        self.ledbank.turnOnLed2()
        return 3

    def mode3(self):
        self.ledbank.turnOnLed3()
        return 4

    def mode4(self):
        self.ledbank.turnOnLed4()
        return 1
