#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
import time
import sys


class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.brightness = 60

    def close(self):
        print("Closing camera.")
        self.camera.close()

    def turnOn(self):
        self.camera.start_preview()

    def turnOff(self):
        self.camera.stop_preview()


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


class ToggleState:
    def __init__(self, starting_state, target):
        self.state = starting_state
        self.target = target

    def toggleState(self):
        self.state = not self.state

        if self.state:
            self.target.turnOn()
        else:
            self.target.turnOff()


class Button:
    last_state=GPIO.HIGH

    def __init__(self, channel):
        self.channel = channel

    def action(self):
        return

    def stateChanged(self, state):
        if state == GPIO.LOW:
            self.action()

    def stateTest(self):
        input_state = GPIO.input(self.channel)
        if input_state != self.last_state:
            self.last_state=input_state
            self.stateChanged(input_state)


class ToggleButton(Button):
    def __init__(self, channel, target):
        Button.__init__(self, channel)
        self.target = target

    def action(self):
        self.target.toggleState()


class VideoButton(Button):
    def __init__(self, channel, led):
        Button.__init__(self, channel)
        self.led = led
        self.camera = None

    def action(self):
        if self.camera is None:
            print("Camera is set to None.  Creating new camera.")
            self.camera = Camera()
            self.camera.turnOn()
            self.led.turnOn()
        else:
            print("Camera is set.  Deleting camera.")
            self.camera.turnOff()
            self.camera.close()
            self.camera = None
            self.led.turnOff()


class Application:
    CHANNEL_SWITCH_MAIN=2
    CHANNEL_SWITCH_SECONDARY=3
    CHANNEL_LED_RED=21
    CHANNEL_LED_YELLOW=16

    sleep_time=0.2

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CHANNEL_SWITCH_MAIN, GPIO.IN)

        self.ledRed = Led(self.CHANNEL_LED_RED, False)
        self.ledYellow = Led(self.CHANNEL_LED_YELLOW, False)

        self.ledRed.turnOff()
        self.ledYellow.turnOn()

        self.videoButton = VideoButton(self.CHANNEL_SWITCH_MAIN, self.ledRed)

    def execute(self):
        self.ledYellow.toggleState()
        self.videoButton.stateTest()

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
            print('Caught eqxception: {0}'.format(e))
            pass


Application().run()

GPIO.cleanup()
print("All done.  Goodbye.");
