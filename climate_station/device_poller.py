import logging
import classes.idleloop as idleloop
from i2c.MCP9808 import MCP9808 as TemperatureSensor
from i2c.HTU21D import HTU21D as HumiditySensor
from i2c.MPL3115A2 import MPL3115A2 as BarometricSensor
from classes.logger import LogManager


class DevicePoller(idleloop.Countdown):
    def __init__(self, sleep):
        idleloop.Countdown.__init__(self, sleep)
        self.log = logging.getLogger('climate-station.DevicePoller')
        self.log.info('Device poller.')

        self.devices = {}
        self.readings = {}

    def dispose(self):
        pass

    def execute(self):
        self.poll_devices()

    def poll_devices(self):
        self.log.debug(self.devices)
        for key in self.devices:
            self.log.debug('polling device: {0}'.format(key))
            value = self.devices[key].read_sensor()
            self.log.debug('value: {}'.format(value))
            self.readings[key] = value

    def add_device(self, name, device):
        if hasattr(device.__class__, 'read_sensor') and callable(getattr(device.__class__, 'read_sensor')):
            self.log.info('register device: {0}'.format(name))
            self.devices[name]  = device
        else:
            self.log.error('add_device: device must have read_sensor() method: {0}'.format(device.__class__))

    def get_readings(self):
        return self.readings
