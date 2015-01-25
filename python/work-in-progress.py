#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys


def set_led(state):
    global LED_STATE
    LED_STATE = state
    print 'New LED state: {0}'.format(LED_STATE)
    GPIO.output(CHANNEL_LED, LED_STATE)


def toggle_led():
    set_led(not(LED_STATE))


def button_changed_state(state):
    if state == GPIO.LOW:
        toggle_led()


def idle_loop():
    global SWITCH_STATE

    while True:
        time.sleep(0.2)
        input_state = GPIO.input(CHANNEL_SWITCH)
        if input_state != SWITCH_STATE:
            SWITCH_STATE=input_state
            button_changed_state(input_state)


def run_application():
    try:
        idle_loop()

    except:
        e = sys.exc_info()[0]
        print 'Caught exception: {0}'.format(e)
        pass


def initialize_application():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_SWITCH, GPIO.IN)
    GPIO.setup(CHANNEL_LED, GPIO.OUT)
    set_led(True)


LED_STATE=True
SWITCH_STATE=GPIO.HIGH

CHANNEL_SWITCH=2
CHANNEL_LED=4

initialize_application()
run_application()

GPIO.cleanup()
print("All done.  Goodbye.");

