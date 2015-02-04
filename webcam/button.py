#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging
from idleloop import Countdown


class Button(Countdown):

    def __init__(self, channel):
        Countdown.__init__(self, 10)

        self.log = logging.getLogger('webcam.Button')
        self.log.info('Instantiate button (channel = ' + str(channel) + ': ' + str(self.__class__))
        self.channel = channel
        self.last_state=GPIO.HIGH

        GPIO.setup(self.channel, GPIO.IN)


    def logDebug(self):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('Button channel: ' + str(self.channel))
            self.log.debug('Button state:   ' + str(self.last_state))


    def actionPressed(self):
        pass


    def actionReleased(self):
        pass


    def stateLow(self):
        self.log.info('Button (channel=' + str(self.channel) + '): button state low')
        self.actionPressed()


    def stateHigh(self):
        self.log.info('Button (channel=' + str(self.channel) + '): button state high')
        self.actionReleased()


    def stateChanged(self, new_state):
        if new_state == GPIO.LOW:
            self.stateLow()
        elif new_state == GPIO.HIGH:
            self.stateHigh()
        else:
            self.log.warning('Button (channel=' + str(self.channel) + '): unknown state')


    def tick(self):
        input_state = GPIO.input(self.channel)
        if input_state != self.last_state:
            self.last_state=input_state
            self.stateChanged(input_state)

