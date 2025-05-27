from machine import Pin, SPI #Import Pin and SPI classes for hardware
import time

class MFRC522:
    OK = 0
    NOTAGERR = 1
    ERR = 2

    REQIDL = 0x26
    AUTH_A = 0x60
    AUTH_B = 0x61

    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs = cs
        self.rst = rst

        self.cs.init(Pin.OUT, value=1)
        self.rst.init(Pin.OUT, value=1)

        self.reset()
        self.write_register(0x2A, 0x8D)
        self.write_register(0x2B, 0x3E)
        self.write_register(0x2D, 30)
        self.write_register(0x2C, 0)
        self.write_register(0x15, 0x40)
        self.write_register(0x11, 0x3D)
        self.antenna_on()

    def write_register(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytearray([(reg << 1) & 0x7E, val]))
        self.cs.value(1)

    def read_register(self, reg):
        self.cs.value(0)
        self.spi.write(bytearray([((reg << 1) & 0x7E) | 0x80]))
        val = self.spi.read(1)[0]
        self.cs.value(1)
        return val

    def set_bit_mask(self, reg, mask):
        self.write_register(reg, self.read_register(reg) | mask)

    def clear_bit_mask(self, reg, mask):
        self.write_register(reg, self.read_register(reg) & (~mask))

    def antenna_on(self):
        if ~(self.read_register(0x14) & 0x03):
            self.set_bit_mask(0x14, 0x03)

    def reset(self):
        self.write_register(0x01, 0x0F)

    def request(self, mode):
        self.write_register(0x0D, 0x07)
        (status, back_data) = self.card_command(0x0C, [mode])
        return status, back_data

    def anticoll(self):
        self.write_register(0x0D, 0x00)
        (status, back_data) = self.card_command(0x0C, [0x93, 0x20])
        if status == self.OK and len(back_data) == 5:
            return self.OK, back_data[:4]
        return self.ERR, None

    def card_command(self, cmd, send_data):
        back_data = []
        back_len = 0
        status = self.ERR
        irq_en = 0x77
        wait_irq = 0x30

        self.write_register(0x02, irq_en | 0x80)
        self.clear_bit_mask(0x04, 0x80)
        self.set_bit_mask(0x0A, 0x80)
        self.write_register(0x01, 0x00)

        for d in send_data:
            self.write_register(0x09, d)

        self.write_register(0x01, cmd)
        if cmd == 0x0C:
            self.set_bit_mask(0x0D, 0x80)

        i = 2000
        while True:
            n = self.read_register(0x04)
            i -= 1
            if (n & 0x01) or (n & wait_irq):
                break
            if i == 0:
                return self.ERR, None

        self.clear_bit_mask(0x0D, 0x80)

        if self.read_register(0x06) & 0x1B:
            return self.ERR, None

        if cmd == 0x0C:
            n = self.read_register(0x0A)
            back_len = n if n < 16 else 16
            back_data = [self.read_register(0x09) for _ in range(back_len)]

        return self.OK, back_data




