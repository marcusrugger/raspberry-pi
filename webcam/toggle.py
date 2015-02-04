#!/usr/bin/python3

import logging
from idleloop import Countdown


class Toggle(Countdown):
    def __init__(self, sleep):
        Countdown.__init__(self, 1)
        self.log = logging.getLogger('webcam.Toggle')
        self.log.info('Instantiate toggle.')

        self.toggle = False


    def toggleOn(self):
        pass


    def toggleOff(self):
        pass


    def execute(self):
        self.toggle = not self.toggle
        if self.toggle:
            self.toggleOn()
        else:
            self.toggleOff()
