import classes.idleloop as idleloop


class Presenter(idleloop.Countdown):
    def __init__(self, sleep, poller, ledbank):
        idleloop.Countdown(self, sleep)

        self.poller     = poller
        self.ledbank    = ledbank
        self.mode       = 1

    def dispose(self):
        pass

    def execute(self):
        if self.mode is 1:
            mode = self.mode1()
        elif self.mode is 2:
            mode = self.mode2()
        elif self.mode is 3:
            mode = self.mode3()
        elif self.mode is 4:
            mode = self.mode4()

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
