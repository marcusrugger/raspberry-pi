#!/usr/bin/python
import classes.idleloop as idleloop
from device_poller import DevicePoller
from datetime import datetime
import json as json


class DataLogger(idleloop.Countdown):
    def __init__(self, sleep, poller):
        idleloop.Countdown.__init__(self, sleep)
        self.poller = poller
        self.location = "living room"
        self.execute()

    def dispose(self):
        self.poller.dispose()

    def execute(self):
        self.poller.poll_devices()

        log = {}
        log["timestamp"]    = datetime.now().isoformat()
        log["location"]     = self.location
        log["temperature"]  = int(10.0 * self.poller.getTemperature() + 0.5) / 10.0
        log["humidity"]     = int(10.0 * self.poller.getHumidity() + 0.5) / 10.0
        log["pressure"]     = int(10.0 * self.poller.getPressure() + 0.5) / 10.0

        print(json.dumps(log))
