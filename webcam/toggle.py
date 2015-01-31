#!/usr/bin/python3

import logging


class Toggle:
    def __init__(self, obj):
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


    def tick(self):
        self.toggle = not self.toggle
        self.logDebug()
        self.obj.set(self.toggle)
