#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys


class Led:
    channel=2
    state=False

    def __init__(self, channel, state):
        self.channel = channel
        self.state = state
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, self.state)

    def set(self, state):
        self.state = state
        GPIO.output(self.channel, self.state)

    def toggleState(self):
        self.set(not self.state)

    def turnOn(self):
        self.set(True)

    def turnOff(self):
        self.set(False)


class ToggleButton:
    last_state=GPIO.HIGH

    def __init__(self, button):
        self.button = button

    def stateChanged(self, state):
        if state == GPIO.LOW:
            self.button.toggleState()

    def stateTest(self):
        input_state = GPIO.input(CHANNEL_SWITCH_MAIN)
        if input_state != self.last_state:
            self.last_state=input_state
            self.stateChanged(input_state)


class Application:
    sleep_time=0.2

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CHANNEL_SWITCH_MAIN, GPIO.IN)

        self.ledRed = Led(CHANNEL_LED_RED, False)
        self.ledYellow = Led(CHANNEL_LED_YELLOW, False)

        self.toggleButton = ToggleButton(self.ledRed)

        self.ledRed.turnOff()
        self.ledYellow.turnOn()

    def execute(self):
        self.toggleButton.stateTest()
        self.ledYellow.toggleState()

    def idle_loop(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(self.sleep_time)
            self.execute()

    def run(self):
        try:
            self.idle_loop()

        except:
            e = sys.exc_info()[0]
            print 'Caught exception: {0}'.format(e)
            pass


CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

application = Application()
application.run()

GPIO.cleanup()
print("All done.  Goodbye.");
