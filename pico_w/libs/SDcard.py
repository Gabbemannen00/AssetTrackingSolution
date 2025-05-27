import machine
import sdcard
import os

sd = sdcard.SDCard(machine.SPI(1), machine.Pin(5))
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# Skriver till SD-kortet
with open('/sd/test.txt', 'w') as f:
    f.write('Hello, SD card!')

# Läser från SD-kortet
with open('/sd/test.txt', 'r') as f:
    print(f.read())
