from machine import Pin, SPI, 
import time
from MFRC522 import MFRC522

# configure SPI
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

# create pin-object for the CS och RST
cs_pin = Pin(17, Pin.OUT)
rst_pin = Pin(22, Pin.OUT)

# Initialize MFRC522 with SPI, CS och RST
rfid = MFRC522(spi, cs_pin, rst_pin)

print("Hold a tag near the reader.")

while True:
    (status, tag_type) = rfid.request(rfid.REQIDL)  # Look for a new tag
    if status != rfid.OK:  # if there is no tagg detected yet
        print("Ingen tagg upptäckt...")
        time.sleep(1) # wait 1 sec until next reading to keep a good flow
    else:
        (status, uid) = rfid.anticoll()  # Read the UID of the tag
        if status == rfid.OK: # if a tag was detected
            print("🎉 RFID-tag discovered! UID:", uid)
            time.sleep(1) # wait 1 sec between tag-detections
            
