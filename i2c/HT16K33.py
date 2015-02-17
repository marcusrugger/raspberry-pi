# LED Display Controller


class HT16K33(object):
    BASE_ADDRESS = 0x70

    REGISTER_DIGIT_1    = 0x00
    REGISTER_DIGIT_2    = 0x02
    REGISTER_DIGIT_3    = 0x06
    REGISTER_DIGIT_4    = 0x08
    REGISTER_COLON      = 0x04

    character_set = [   0x3f,   # 0
                        0x06,   # 1
                        0x5b,   # 2
                        0x4f,   # 3
                        0x66,   # 4
                        0x6d,   # 5
                        0x7d,   # 6
                        0x07,   # 7
                        0x7f,   # 8
                        0x6f    # 9
                    ]

    def __init__(self, device):
        self.device = device

        self.turnOffDisplay()
        self.turnOffOscillator()
        self.setDimming(15)

        with self.device as bus:
            bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_1, 0x00)
            bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_2, 0x00)
            bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_3, 0x00)
            bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_4, 0x00)
            bus.writeByteToRegister(HT16K33.REGISTER_COLON,   0x00)

    def dispose(self):
        self.turnOffDisplay()
        self.turnOffOscillator()

    def turnOnOscillator(self):
        with self.device as bus : bus.writeByte(0x21)

    def turnOffOscillator(self):
        with self.device as bus : bus.writeByte(0x20)

    def turnOnDisplay(self):
        with self.device as bus : bus.writeByte(0x81)

    def turnOffDisplay(self):
        with self.device as bus : bus.writeByte(0x80)

    def setDimming(self, dim):
        if   dim <  0 : dim = 0
        elif dim > 15 : dim = 15
        with self.device as bus : bus.writeByte(0xe0 | int(dim))

    def setColon(self, flag):
        with self.device as bus : bus.writeByteToRegister(HT16K33.REGISTER_COLON, 0xff if flag else 0x00)

    def writeNumber(self, number):
        d4 = number % 10

        number = int(number/10)
        d3 = number % 10

        number = int(number/10)
        d2 = number % 10

        number = int(number/10)
        d1 = number % 10

        self._writeDigits(d1, False, d2, False, d3, False, d4, False)

    def writeFixedPoint(self, number):
        number = int(10 * number + 0.5)
        d4 = number % 10

        number = int(number/10)
        d3 = number % 10

        number = int(number/10)
        d2 = number % 10

        number = int(number/10)
        d1 = number % 10

        self._writeDigits(d1, False, d2, False, d3, True, d4, False)

    def _writeDigits(self, d1, d1Dot, d2, d2Dot, d3, d3Dot, d4, d4Dot):
        try:
            with self.device as bus:
                print_zeros = d1 > 0 or d1Dot
                if print_zeros:
                    self._writeDigit(bus, HT16K33.REGISTER_DIGIT_1, d1, d1Dot)
                else:
                    bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_1, 0x00)

                print_zeros = print_zeros or d2 > 0 or d2Dot
                if print_zeros:
                    self._writeDigit(bus, HT16K33.REGISTER_DIGIT_2, d2, d2Dot)
                else:
                    bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_2, 0x00)

                print_zeros = print_zeros or d3 > 0 or d3Dot
                if print_zeros:
                    self._writeDigit(bus, HT16K33.REGISTER_DIGIT_3, d3, d3Dot)
                else:
                    bus.writeByteToRegister(HT16K33.REGISTER_DIGIT_3, 0x00)

                self._writeDigit(bus, HT16K33.REGISTER_DIGIT_4, d4, d4Dot)
        except OSError as e:
            print('HT16K33: _writeDigits: Caught exception: {0}'.format(e))
            raise

    def _writeDigit(self, bus, position, number, dotOn=False):
        bitmap = HT16K33.character_set[number]
        if dotOn : bitmap = bitmap | 0x80
        try:
            bus.writeByteToRegister(position, bitmap)
        except OSError as e:
            print('HT16K33: _writeDigit: Caught exception: {0}'.format(e))
            raise
