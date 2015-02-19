import logging
import classes.idleloop as idleloop
from i2c.MCP9808 import MCP9808 as TemperatureSensor
from i2c.HTU21D import HTU21D as HumiditySensor
from i2c.MPL3115A2 import MPL3115A2 as BarometricSensor
from classes.logger import LogManager


class DevicePoller(idleloop.Countdown):
    def __init__(self, sleep, thermometer, hygrometer, barometer):
        idleloop.Countdown.__init__(self, sleep)
        self.log = logging.getLogger('climate-station.DevicePoller')
        self.log.info('Device poller.')

        self.thermometer    = thermometer
        self.hygrometer     = hygrometer
        self.barometer      = barometer

        self.temperature    = {}
        self.humidity       = {}
        self.pressure       = {}

    def dispose(self):
        self.thermometer.dispose()
        self.hygrometer.dispose()
        self.barometer.dispose()

    def execute(self):
        self.poll_devices()

    def poll_devices(self):
        self._pollThermometer();
        self._pollHygrometer();
        self._pollBarometer();

    def _pollThermometer(self):
        try:
            self.temperature = self.thermometer.read_sensor()
        except OSError as e:
            self.log.error(e)

    def _pollHygrometer(self):
        try:
            self.humidity = self.hygrometer.read_sensor()
        except OSError as e:
            self.log.error(e)

    def _pollBarometer(self):
        try:
            self.pressure = self.barometer.read_sensor()
        except OSError as e:
            self.log.error(e)

    def getTemperature(self):
        return self.temperature['temperature']['fahrenheit']

    def getHumidity(self):
        return self.humidity['humidity']['relative']

    def getPressure(self):
        return self.pressure['pressure']['inHg']

    def getAllTemperature(self):
        return self.temperature

    def getAllHumidity(self):
        return self.humidity

    def getAllPressure(self):
        return self.pressure
