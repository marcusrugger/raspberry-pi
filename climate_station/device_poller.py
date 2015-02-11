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

    def dispose(self):
        self.thermometer.dispose()
        self.hygrometer.dispose()
        self.barometer.dispose()

    def execute(self):
        self.temperature    = thermometer.read_sensor()
        self.humidity       = hygrometer.read_sensor()
        self.pressure       = barometer.read_sensor()

    def temperature(self):
        return self.temperature['fahrenheit']

    def humidity(self):
        return self.humidity['humidity']

    def pressure(self):
        return self.pressure['pressure']
