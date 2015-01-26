#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys


class Led:
    mChannel=2
    mState=False

    def __init__(self, channel, state):
        mChannel = channel
        mState = state
        GPIO.output(mChannel, mState)

    def toggleState():
        mState = not mState
        GPIO.output(mChannel, mState)


def button_changed_state(state):
    if state == GPIO.LOW:
        buttonRed.toggleState()


def process_main_button():
    global SWITCH_STATE

    input_state = GPIO.input(CHANNEL_SWITCH_MAIN)
    if input_state != SWITCH_STATE:
        SWITCH_STATE=input_state
        button_changed_state(input_state)


def execute():
    process_main_button()


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
    global buttonRed
    global buttonYellow
    buttonRed = Led(CHANNEL_LED_RED, False)
    buttonYellow = Led(CHANNEL_LED_YELLOW, False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_SWITCH_MAIN, GPIO.IN)
    GPIO.setup(CHANNEL_LED_RED, GPIO.OUT)
    GPIO.setup(CHANNEL_LED_YELLOW, GPIO.OUT)
    GPIO.output(CHANNEL_LED_YELLOW, True)
    set_led(True)
    

STATE_LED_RED=True
SWITCH_STATE=GPIO.HIGH

CHANNEL_SWITCH_MAIN=2
CHANNEL_SWITCH_SECONDARY=3
CHANNEL_LED_RED=21
CHANNEL_LED_YELLOW=16

keepRunning = True

initialize_application()
run_application()

GPIO.cleanup()
print("All done.  Goodbye.");

