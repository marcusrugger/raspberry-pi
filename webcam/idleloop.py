#!/usr/bin/python3

import time
import logging


class Countdown:
    def __init__(self, countdown):
        self.countdown_reset = countdown
        self.countdown = countdown


    def tick(self):
        self.countdown = self.countdown - 1
        if self.countdown < 1:
            self.countdown = self.countdown_reset
            self.execute()


class IdleLoop:
    TICKS_PER_SECOND = 10
    RESOLUTION = (1 / TICKS_PER_SECOND)

    def __init__(self):
        self.log = logging.getLogger('webcam.IdleLoop')
        self.log.info('Instantiate idle loop.')

        self.sleep = IdleLoop.RESOLUTION
        self.isDone = False
        self.registrants = []


    def __enter__(self):
        return self


    def disposeOf(self, obj):
        if hasattr(obj.__class__, 'dispose') and callable(getattr(obj.__class__, 'dispose')):
            self.log.info('Dispose object: {0}.'.format(obj.__class__))
            obj.dispose()


    def __exit__(self, type, value, traceback):
        self.log.info('Dispose registrants.')
        for registrant in self.registrants : self.disposeOf(registrant)


    def setDone(self, flag):
        self.isDone = flag


    def register(self, registrant):
        self.registrants.append(registrant)


    def unregister(self, registrant):
        self.registrants.remove(registrant)


    def tick(self):
        for registrant in self.registrants : registrant.tick()


    def run(self):
        while not self.isDone:
            time.sleep(self.sleep)
            self.tick()