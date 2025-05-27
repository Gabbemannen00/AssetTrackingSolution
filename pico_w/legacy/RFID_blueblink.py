from machine import Pin, SPI
import time
from MFRC522 import MFRC522

# SPI-inställningar för RFID
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cs_pin = Pin(17, Pin.OUT)
rst_pin = Pin(22, Pin.OUT)
rfid = MFRC522(spi, cs_pin, rst_pin)

# LED
blue_led = Pin(13, Pin.OUT)

# Blink-variabler
blue_led_state = False
last_blink_time = time.ticks_ms()

print("Startar RFID-läsaren...")

while True:
    try:
        # Blinkar blå LED var 200 ms
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_blink_time) > 200:
            blue_led_state = not blue_led_state
            blue_led.value(blue_led_state)
            last_blink_time = current_time

        # Kolla efter en tagg med längre timeout (1 sekund)
        start_time = time.ticks_ms()
        status = None
        uid = None  # UID ska vara None från början
        while time.ticks_diff(time.ticks_ms(), start_time) < 1000:  # Timeout på 1000 ms
            (status, tag_type) = rfid.request(rfid.REQIDL)
            if status == rfid.OK:
                # Försök läsa UID från taggen
                (status, uid) = rfid.anticoll()
                if status == rfid.OK and uid:
                    break  # Tagg hittad, gå vidare

        if status == rfid.OK and uid:
            # Stäng av blå LED när tagg hittas
            blue_led.value(0)
            print(f"🎉 Tagg upptäckt! UID: {uid}")
            time.sleep(0.5)  # Vänta lite innan ny avläsning
        else:
            # Om ingen giltig tagg hittas
            print("Ingen tagg detekterad.")
            time.sleep(1) #lägg till en liten fördröjning

    except Exception as e:
        print("Fel:", e)
