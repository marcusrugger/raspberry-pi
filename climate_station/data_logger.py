#!/usr/bin/python
import classes.idleloop as idleloop
from device_poller import DevicePoller


class DataLogger(idleloop.Countdown):
    def __init__(self, sleep, poller):
        idleloop.Countdown.__init__(self, sleep)
        self.poller = poller
        self.execute()

    def dispose(self):
        pass

    def execute(self):
        temperature = self.poller.getTemperature()
        humidity    = self.poller.getHumidity()
        pressure    = self.poller.getPressure()
        print("temperature: {:5.1f}, humidity {:4:1}, pressure: {:4.1}", temperature, humidity, pressure)
