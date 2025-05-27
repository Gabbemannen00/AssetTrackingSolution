from machine import Pin,PWM, SPI, I2C
from i2c_lcd import I2cLcd
import time
from MFRC522 import MFRC522

# Konfigurera SPI för MFRC522-modulen
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

# Skapa Pin-objekt för CS och RST
cs_pin = Pin(17, Pin.OUT)
rst_pin = Pin(22, Pin.OUT)

# Initiera MFRC522 med SPI, CS och RST
rfid = MFRC522(spi, cs_pin, rst_pin)

 # configure buzzer (connect the buzzers (+) to pico GP16 and (-) to GND) 
buzzer = PWM(Pin(16))
    
# Konfigurera LED:er (grön, röd, blå LED)
green_led = Pin(14, Pin.OUT)  # Green LED
red_led = Pin(15, Pin.OUT)    # Red LED
blue_led = Pin(13, Pin.OUT)   # Blue LED
yellow_led = Pin(8, Pin.OUT)    # Yellow LED
        
# Konfiguera valda enheters UID
RFID_CARD = [148, 195, 163, 219] #kortets UID
RFID_TAG = [65, 36, 32, 76] #taggens UID

# Konfiguera LCD Använd GP4 & GP5 för standard I2C0, eller GP0 & GP1 för I2C1
I2C_SDA = Pin(4)  
I2C_SCL = Pin(5)  
i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=100000)  

#starta programmet alltid med lamporna avstängda
green_led.value(0)
red_led.value(0)
blue_led.value(0)

# funktion för att få buzzern att pipa. Ljudet kan modifieras
# genom att ändra varaktighet, volym eller frekvens närhelst man känner för det
    
def beep(duration=0.1, volume=20000, frequency=4000):
    buzzer.freq(frequency)
    buzzer.duty_u16(volume)
    time.sleep(duration)
    buzzer.duty_u16(0) #initialize the active buzzer and will only be activated when being called
    
def leds_on():
    green_led.value(1)
    red_led.value(1)
    blue_led.value(1)

# Funktion för att stänga av alla LED:er

def leds_off():
    green_led.value(0)
    red_led.value(0)
    blue_led.value(0)

# Funktion för att skapa ett flytande regnbågsljus mellan lamporna.
def rainbow_leds():
    times = 0
    times_opposite = 0
    max = 30
    while times < max:
        red_led.value(0.5)
        beep(duration=0.1, volume=10000, frequency=2000)
        time.sleep(0.1)
        red_led.value(0)
        blue_led.value(0.5)
        beep(duration=0.1, volume=12000, frequency=1600)
        time.sleep(0.1)
        blue_led.value(0)
        green_led.value(0.5)
        beep(duration=0.1, volume=4500, frequency=1200)
        time.sleep(0.1)
        green_led.value(0)
        time.sleep(0.1)
        
        leds_on()
        beep(duration=0.1, volume=1500, frequency=1100)
        time.sleep(0.1)
        leds_off()
        time.sleep(0.1)
        leds_on()
        beep(duration=0.1, volume=2500, frequency=770)
        time.sleep(0.1)
        leds_off()
        time.sleep(0.1)
        leds_on()
        beep(duration=0.1, volume=3500, frequency=850)
        time.sleep(0.1)
        leds_off()
        time.sleep(0.1)
        times+=1
        #print("Från röd till blå, från blå till grön antal gånger: ",times)
        if times == 15: #Kör max 15 iterationer på detta sätt.
            break
        
    while times < max: #byt sedan till denna loop som ska köra i motsatt riktning
        green_led.value(0.5)
        beep(duration=0.1, volume=1000, frequency=800)
        time.sleep(0.1)
        green_led.value(0)
        blue_led.value(0.5)
        beep(duration=0.1, volume=2000, frequency=700)
        time.sleep(0.1)
        blue_led.value(0)
        red_led.value(0.5)
        beep(duration=0.1, volume=3000, frequency=600)
        time.sleep(0.1)
        red_led.value(0)
        times_opposite+=1
        #print("Från grön till blå, från blå till röd antal gånger: ",times_opposite)
        if times_opposite == 15:
            break
               
# Funktion för att visa grönt ljus när UID är läst
def green_light():
    print("grön lampa på!")
    green_led.value(1)
    red_led.value(0)
    blue_led.value(0)

# Funktion för det röda ljuset när UID inte kunde läsas
def red_light():
    print("röd lampa på!")
    blue_led.value(0)
    #blinka röd lampa en mycket kort stund när taggens UID identifieras
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    time.sleep(0.1)
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    time.sleep(0.1)
    
# Funktion för att visa blått blinkande ljus för att indikera att läsaren söker
def blue_blink():
    print("blå lampa blinkar!")
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    blue_led.value(1)
    time.sleep(0.3)
    blue_led.value(0)
       
# Leta efter I2C-enheter
i2c_addresses = i2c.scan()
print(f"✅ Found I2C devices at address: {[hex(address) for address in i2c_addresses]}")
print("Kolla din LCD om du ser text.")


if not i2c_addresses: #om ingen I2C-enhet hittas
    print("🚫 No I2C-device was found")
else:
    #print(f"✅ I2C-devices found at addresses: {', '.join(hex(addr) for addr in i2c_addresses)}")
    lcd = I2cLcd(i2c, 0x27, 2, 16)  # LCD med adress 0x27
    lcd.putstr("LCD: ansluten")
    lcd.move_to(0,1)
    lcd.putstr("adress: 0x27")
    time.sleep(2)
    lcd.clear()

print("⏳Startar RFID läsare...")
print("🎵 En vacker sång från buzzern hörs medans du väntar")

lcd.putstr("RFID: Startar...")
lcd.move_to(0,1)
lcd.putstr("Ljud och lampor på")

#rainbow_leds()

lcd.clear()
time.sleep(0.2)
leds_on()
time.sleep(0.1)
leds_off()
beep(duration= 0.1, volume= 13000, frequency=2000)
leds_on()
time.sleep(0.1)
leds_off()
beep(duration= 0.1, volume= 15000, frequency=3000)
leds_on()
time.sleep(0.1)
leds_off()
beep(duration= 0.1, volume= 17000, frequency=4000)
leds_on()

lcd.putstr("RFID: Ansluten")
lcd.move_to(0,1)
lcd.putstr("Skanna tagg/kort")

print("")
print("✅ RFID På.")
print("📡 Nu kan du hålla en RFID-tagg nära läsaren.")
print("🏷️ Kollar efter en tagg...")
print("")

time.sleep(2)

leds_off()

times_card = 0 #kort skanningar
times_tag = 0 # tagg skanningar
times_unknown = 0 #antalet skanningar av okänd tagg/kort

while True:
    try:
        (status, tag_type) = rfid.request(rfid.REQIDL)  # Kolla efter en ny tagg
        
    except Exception as e:
        print("Fel vid kommunikation med RFID-läsaren:", e)
        lcd.putstr("RFID: funnet Error!")
        lcd.move_to(0,1)
        lcd.putstr("Kolla jumperkablar.")
        continue #försök igen om ett fel inträffar
    
    # Kolla efter en tagg och säkerställ att blå LED blinkar när ingen tagg finns
    if status != rfid.OK:  # Ingen tagg finns
        print("Ingen tagg detekterad. Blå LED blinkar.")
        while True:
            blue_blink()
            (status, tag_type) = rfid.request(rfid.REQIDL)
            if status == rfid.OK:
                blue_led.value(0)
                break
                    
    else:
        (status, uid) = rfid.anticoll()  # Läs UID från taggen
        if status == rfid.OK and uid:
            uid_list = list(uid)
            print("")
            print("🎉 Tagg eller kort upptäckt! UID:", uid_list)
            print("")
            if uid_list == RFID_CARD:
               lcd.clear()
               times_card+=1 #registrera antalet blipp
               green_light() #tänd grön lampa i takt med ljudets längd från buzzern
               lcd.putstr("RFID: kontakt!")
               lcd.move_to(0,1)
               lcd.putstr("Gabriels kort   ")
               print("Du blippade ditt RFID-kort!")
               beep(duration = 0.3, volume= 18000, frequency= 4000)
               blue_blink()
               print(f"Du har blippat kortet {times_card} gånger.")
               time.sleep(0.5)  # Vänta lite innan släckning
               green_led.value(0)  # Släck lampan helt
               time.sleep(0.5) # vänta en halv sekund innan nästa blipp tas in
            elif uid_list == RFID_TAG:
                lcd.clear()
                times_tag+=1
                red_light() #blinka röd lampa i takt med ljudet från buzzern
                lcd.putstr("RFID: kontakt!")
                lcd.move_to(0,1)#skriv ut på nedre raden av LCD:n
                lcd.putstr("Gabriels tagg (=")
                print("Du blippade din RFID-tagg!")
                beep(duration = 0.1, volume= 20000, frequency= 3000)
                time.sleep(0.1)
                beep(duration = 0.1, volume= 20000, frequency= 3000)
                blue_blink()
                print(f"Du har blippat taggen {times_tag} gånger.")
                time.sleep(0.5)  # Vänta lite innan släckning
                red_led.value(0)  # Släck efter blippning
                time.sleep(0.5)
            else:
                times_unknown+=1
                red_light()
                lcd.putstr("RFID: kontakt!")
                lcd.move_to(0,1)#skriv ut på nedre raden av LCD:n
                lcd.putstr("UID: unknown )=")
                print("Okänd enhet!")
                print(f"Du har blippat okända enheter {times_unknown} gånger.")
                beep(0.7, volume= 13000, frequency = 500)
                time.sleep(1)
                
            
               
            
            

