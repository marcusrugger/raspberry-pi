import classes.idleloop as idleloop
from i2c.MCP9808 import MCP9808 as TemperatureSensor
from i2c.HTU21D import HTU21D as HumiditySensor
from i2c.MPL3115A2 import MPL3115A2 as BarometricSensor


class DevicePoller(idleloop.Countdown):
    def __init__(self, sleep, thermometer, hygrometer, barometer):
        idleloop.Countdown.__init__(self, sleep)

        self.thermometer    = thermometer
        self.hygrometer     = hygrometer
        self.barometer      = barometer

        self.execute()

    def dispose(self):
        self.thermometer.dispose()
        self.hygrometer.dispose()
        self.barometer.dispose()

    def execute(self):
        self.poll_devices()

    def poll_devices(self):
        self.temperature    = self.thermometer.read_sensor()
        self.humidity       = self.hygrometer.read_sensor()
        self.pressure       = self.barometer.read_sensor()

    def getTemperature(self):
        return self.temperature['fahrenheit']

    def getHumidity(self):
        return self.humidity['humidity']

    def getPressure(self):
        return self.pressure['pressure']

    def getAllTemperature(self):
        return self.temperature

    def getAllHumidity(self):
        return self.humidity

    def getAllPressure(self):
        return self.pressure
