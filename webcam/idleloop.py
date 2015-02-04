#!/usr/bin/python3

import time
import logging


class Countdown:
    def __init__(self, sleep):
        self.timestamp = time.time()
        self.sleep = sleep


    def tick(self, timestamp):
        if timestamp - self.timestamp >= self.sleep:
            self.timestamp = timestamp
            self.execute()


class IdleLoop:
    TICKS_PER_SECOND = 10
    RESOLUTION = (1 / TICKS_PER_SECOND)

    def __init__(self):
        self.log = logging.getLogger('webcam.IdleLoop')
        self.log.info('Instantiate idle loop.')

        self.isDone = False
        self.registrants = []


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.log.info('Dispose registrants.')
        for registrant in self.registrants : self.disposeOf(registrant)


    def disposeOf(self, obj):
        if hasattr(obj.__class__, 'dispose') and callable(getattr(obj.__class__, 'dispose')):
            self.log.info('Dispose object: {0}.'.format(obj.__class__))
            obj.dispose()


    def setDone(self, flag):
        self.isDone = flag


    def register(self, registrant):
        if hasattr(registrant.__class__, 'tick') and callable(getattr(registrant.__class__, 'tick')):
            self.registrants.append(registrant)
        else:
            self.log.error('register: registrant must have tick() method: {0}'.format(registrant.__class__))


    def unregister(self, registrant):
        self.registrants.remove(registrant)


    def tick(self, timestamp):
        for registrant in self.registrants : registrant.tick(timestamp)


    def run(self):
        timestamp = time.time()
        while not self.isDone:
            sleep_time = IdleLoop.RESOLUTION - (time.time() - timestamp)
            if sleep_time > 0 : time.sleep(sleep_time)
            timestamp = time.time()
            self.tick(timestamp)
