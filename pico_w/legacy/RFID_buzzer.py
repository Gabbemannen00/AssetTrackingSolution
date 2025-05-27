from machine import Pin, PWM, SPI
import time
from MFRC522 import MFRC522

# Configure SPI
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

# create Pin-object for CS och RST
cs_pin = Pin(17, Pin.OUT)
rst_pin = Pin(22, Pin.OUT)

# Initialize MFRC522 with SPI, CS och RST
rfid = MFRC522(spi, cs_pin, rst_pin)

# Configure buzzer (connect the buzzers (+) to pico GP16 and (-) to GND)
buzzer = PWM(Pin(16))
    
    # function for making the buzzer to beep. The sound can be modified
    # by changing the duration, volume or frequency as you wish.
    
def beep(duration=0.1, volume=20000, frequency=4000):
    buzzer.freq(frequency)
    buzzer.duty_u16(volume)
    
    time.sleep(duration)
    
    buzzer.duty_u16(0) #initialize the active buzzer and will only be activated when being called.

#Identify which UID belongs to the card or the tag
RFID_CARD= [148, 195, 163, 219]
RFID_TAG= [65, 36, 32, 76]

#tracking the amount of times
times_card = 0
times_tag = 0
times_unknown = 0

print("Håll en RFID-tagg eller kort nära läsaren.")
print("Söker efter enhet...")
print("")

while True:
    # Kolla efter en tagg och säkerställ att blå LED blinkar när ingen tagg finns
    (status, tag_type) = rfid.request(rfid.REQIDL)  # Kolla efter en ny tagg
    if status != rfid.OK:  # Ingen tagg finns
        print("Ingen tagg detekterad.")
        time.sleep(1)
    else:
        (status, uid) = rfid.anticoll()  # Läs UID från taggen
        if status == rfid.OK:
            print("🎉 RFID-tagg upptäckt! UID:", uid)
            beep(0.3) # ljud för att en skanning har lyckats.
            time.sleep(0.1)
            if uid == RFID_CARD:
                times_card+=1
                print("Du blippade ditt RFID-kort!")
                beep(duration=0.2, volume =5000, frequency= 1000) #ljud som identifierar om vad det är som har skannats.
                time.sleep(0.1)
                print(f"Du har blippat kortet {times_card} gånger.")
                beep(duration=0.2, volume =5000, frequency= 1000)
                print("")
                time.sleep(1) #vänta 1 sekund innan nästa läsning
            elif uid == RFID_TAG:
                times_tag+=1
                print("Du blippade din RFID-tagg!")
                beep(duration=0.1, volume =8000, frequency= 2500)
                time.sleep(0.1)
                beep(duration=0.1, volume =8000, frequency= 2500)
                time.sleep(0.2)
                print(f"Du har blippat taggen {times_tag} gånger.")
                print("")
                time.sleep(1) #vänta 1 sekund innan nästa läsning
            else:
                times_unknown+=1
                print("Du blippade en okänd enhet!")
                beep(duration=0.7, volume =15000, frequency= 500)
                time.sleep(0.2)
                print(f"antal blipp: {times_unknown} gånger.")
                print("")
                time.sleep(1)
            
            
