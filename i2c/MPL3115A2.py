# Barometer/Altimeter
import time
import struct
from datetime import datetime


def celsius_to_fahrenheit(celsius):
    return 1.8 * celsius + 32.0

def round_one_decimal(value):
    return int(10 * value) / 10.0

def round_two_decimal(value):
    return int(100 * value) / 100.0


class MPL3115A2(object):
    BASE_ADDRESS = 0x60

    REGISTER_STATUS                 = 0x00
    REGISTER_STATUS_TDR             = 0x02  # New measurement ready to be read
    REGISTER_STATUS_PDR             = 0x04  # New measurement ready to be read
    REGISTER_STATUS_PTDR            = 0x08  # New measurement ready to be read
    REGISTER_STATUS_DATA_READY      = (REGISTER_STATUS_TDR | REGISTER_STATUS_PDR | REGISTER_STATUS_PTDR)

    REGISTER_F_SETUP                = 0x0f
    REGISTER_F_SETUP_FIFO_DISABLE   = 0x00

    REGISTER_PT_DATA_CFG            = 0x13
    REGISTER_PT_DATA_CFG_TDEFE      = 0x01  # Raise event flag on new temperature data
    REGISTER_PT_DATA_CFG_PDEFE      = 0x02  # Raise event flag on new pressure data
    REGISTER_PT_DATA_CFG_DREM       = 0x04  # Generate data ready event

    REGISTER_CONTROL                = 0x26
    REGISTER_CONTROL_SBYB           = 0x01  # Sets mode to active (1 = active, 0 = standby)
    REGISTER_CONTROL_OST            = 0x02  # Initiate measurement immediately
    REGISTER_CONTROL_RST            = 0x04  # Software reset
    REGISTER_CONTROL_OS0            = 0x08  # Oversample ratio (000), bit 1
    REGISTER_CONTROL_OS1            = 0x10  # Oversample ratio (000), bit 2
    REGISTER_CONTROL_OS2            = 0x20  # Oversample ratio (000), bit 3
    REGISTER_CONTROL_OS000          = 0x00  # Oversample ratio of 0
    REGISTER_CONTROL_OS111          = (REGISTER_CONTROL_OS0 | REGISTER_CONTROL_OS1 | REGISTER_CONTROL_OS2)
    REGISTER_CONTROL_RAW            = 0x40  # Raw output mode
    REGISTER_CONTROL_ALT            = 0x90  # Altimeter mode (1 = Altimeter, 0 = Barometer)

    PASCALS_PER_INCH_OF_MERCURY     = 3386.389


    def __init__(self, bus):
        self.bus = bus

        with bus as device:
            device.writeByteToRegister(MPL3115A2.REGISTER_F_SETUP,     MPL3115A2.REGISTER_F_SETUP_FIFO_DISABLE)
            device.writeByteToRegister(MPL3115A2.REGISTER_PT_DATA_CFG, MPL3115A2.REGISTER_PT_DATA_CFG_DREM  |
                                                                       MPL3115A2.REGISTER_PT_DATA_CFG_PDEFE |
                                                                       MPL3115A2.REGISTER_PT_DATA_CFG_TDEFE)
            device.writeByteToRegister(MPL3115A2.REGISTER_CONTROL,     0x00)

    def dispose(self):
        with self.bus as device:
            device.writeByteToRegister(MPL3115A2.REGISTER_PT_DATA_CFG, 0x00)
            device.writeByteToRegister(MPL3115A2.REGISTER_CONTROL, 0x00)

    def read_sensor(self):
        print("Barometer read_sensor")
        with self.bus as device:
            self._initiateMeasurement(device)
            raw = device.readBytes(6)
            #self._setDeviceToStandby(device)

        status, pmsb, pcsb, plsb, tmsb, tlsb = struct.unpack("6B", raw)

        register_pressure    = (pmsb << 16) | (pcsb << 8) | plsb
        register_temperature = (tmsb << 8) | tlsb

        pascals     = register_pressure / 64.0
        inHg        = pascals / MPL3115A2.PASCALS_PER_INCH_OF_MERCURY
        celsius     = register_temperature / 256.0
        fahrenheit  = celsius_to_fahrenheit(celsius)

        rv = {}

        rv['timestamp']     = datetime.now().isoformat()
        rv['pressure']      = {}
        rv['temperature']   = {}

        rv['pressure']['register']  = hex(register_pressure)
        rv['pressure']['pascals']   = round_one_decimal(pascals)
        rv['pressure']['inHg']      = round_two_decimal(inHg)

        rv['temperature']['register']   = hex(register_temperature)
        rv['temperature']['celsius']    = round_one_decimal(celsius)
        rv['temperature']['fahrenheit'] = round_one_decimal(fahrenheit)

        return rv

    def _initiateMeasurement(self, device):
        device.writeByteToRegister(MPL3115A2.REGISTER_CONTROL, MPL3115A2.REGISTER_CONTROL_SBYB |
                                                               MPL3115A2.REGISTER_CONTROL_OST  |
                                                               MPL3115A2.REGISTER_CONTROL_OS111)

        status = 0
        while (status & MPL3115A2.REGISTER_STATUS_DATA_READY) != MPL3115A2.REGISTER_STATUS_DATA_READY:
            time.sleep(0.1)
            status = device.readByteFromRegister(MPL3115A2.REGISTER_STATUS)
            print("status: 0x{:02x}".format(status))

    def _setDeviceToStandby(self, device):
        device.writeByteToRegister(MPL3115A2.REGISTER_PT_DATA_CFG, 0x00)
        device.writeByteToRegister(MPL3115A2.REGISTER_CONTROL, 0x00)


if __name__ == "__main__":
    from py2cbus import i2c
    print("Testing MPL3115A2...")
    barometer = MPL3115A2(i2c(1, MPL3115A2.BASE_ADDRESS))
    rv = barometer.read_sensor()
    print("Sensor: {}".format(rv))
