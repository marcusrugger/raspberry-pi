#!/usr/bin/python3

import logging
from toggle import Toggle
from led import Led


class ToggleLed(Toggle, Led):
    def __init__(self, sleep, channel, state):
        Toggle.__init__(self, sleep)
        Led.__init__(self, channel, state)
        self.log = logging.getLogger('webcam.ToggleLed')
        self.log.info('Instantiate toggle.')


    def toggleOn(self):
        Led.turnOn(self)


    def toggleOff(self):
        Led.turnOff(self)
