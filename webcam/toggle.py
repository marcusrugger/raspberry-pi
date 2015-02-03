#!/usr/bin/python3

import logging
from idleloop import Countdown
from idleloop import IdleLoop


class Toggle(Countdown):
    def __init__(self, obj):
        Countdown.__init__(self, IdleLoop.TICKS_PER_SECOND)
        self.log = logging.getLogger('webcam.Toggle')
        self.log.info('Instantiate toggle.')

        self.obj = obj
        self.toggle = False

        self.logDebug()


    def dispose(self):
        if hasattr(self.obj.__class__, 'dispose') and callable(getattr(self.obj.__class__, 'dispose')):
            self.log.info('Dispose object: {0}.'.format(self.obj.__class__))
            self.obj.dispose()


    def logDebug(self):
        self.log.debug('Object: ' + str(self.obj.__class__))
        self.log.debug('Toggle: ' + str(self.toggle))


    def execute(self):
        self.toggle = not self.toggle
        self.logDebug()
        self.obj.set(self.toggle)
