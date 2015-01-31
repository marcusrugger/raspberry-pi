#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging


class Button:

    def __init__(self, channel):
        self.log = logging.getLogger('webcam.Button')
        self.log.info('Instantiate button (channel = ' + str(channel) + ': ' + str(self.__class__))

        self.channel = channel
        self.last_state=GPIO.HIGH

        GPIO.setup(self.channel, GPIO.IN)


    def logDebug(self):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('Button channel: ' + str(self.channel))
            self.log.debug('Button state:   ' + str(self.last_state))


    def action(self):
        return


    def stateChanged(self, state):
        if state == GPIO.LOW:
            self.log.info('Button (channel=' + str(self.channel) + '): excecute action')
            self.action()


    def tick(self):
        input_state = GPIO.input(self.channel)
        if input_state != self.last_state:
            self.last_state=input_state
            self.stateChanged(input_state)

