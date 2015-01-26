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
            last_state=input_state
            self.stateChanged(input_state)



def execute():
    toggleButton.stateTest()
    ledYellow.toggleState()


def idle_loop():
    global keepRunning

    while keepRunning:
        time.sleep(0.2)
        execute()


def run_application():
    try:
        idle_loop()

    except:
        e = sys.exc_info()[0]
        print 'Caught exception: {0}'.format(e)
        pass


def initialize_application():
    global toggleButton
    global ledRed
    global ledYellow

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_SWITCH_MAIN, GPIO.IN)

    ledRed = Led(CHANNEL_LED_RED, False)
    ledYellow = Led(CHANNEL_LED_YELLOW, False)

    toggleButton = ToggleButton(ledRed)

    ledRed.turnOff()
    ledYellow.turnOn()


CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

keepRunning = True

initialize_application()
run_application()

GPIO.cleanup()
print("All done.  Goodbye.");
