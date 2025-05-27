import time
from machine import Pin, I2C, SPI, PWM
from MFRC522 import MFRC522

"""Read UID from a RFID-tag and print it on the LCD, using LEDS and Buzzer,
The point of this code is not only to check if the reader or a tag is functional
, but also if a tags UID is recognized or not in the list of allowed tags . If
it"""

 # configure buzzer (connect the buzzers (+) to pico GP16 and (-) to GND)
buzzer = PWM(Pin(16))

# Declaring a function for changing the sound of the buzzer. The sound can
# be modified by changing the duration, volume or frequency whenever it fits you
    
def beep(duration=0.1, volume=20000, frequency=4000):
    """Play a beep-sound with the buzzer"""
    buzzer.freq(frequency)
    buzzer.duty_u16(volume)
    time.sleep(duration)
    buzzer.duty_u16(0) #initialize the buzzer offline, and will only be activated when calling the function "beep"

#----------------------------------------------------------------------------------------

# Configure all LED:S (green, red, blue)
green_led = Pin(14, Pin.OUT)  # Green LED connected to GP14
red_led = Pin(15, Pin.OUT)    # Red LED connected to GP15
blue_led = Pin(13, Pin.OUT)   # Blue LED connected GP13
yellow_led =Pin(8, Pin.OUT)   # Yellow LED connected GP8

# Start the program always with the LED:s set to off
green_led.value(0)
red_led.value(0)
blue_led.value(0)
yellow_led.value(0)


# Function for starting all the LED:s at once
def leds_on():
    green_led.value(1)
    red_led.value(1)
    blue_led.value(1)
    yellow_led.value(1)

# Function for shutting off all the LED:s at once
def leds_off():
    green_led.value(0)
    red_led.value(0)
    blue_led.value(0)
    yellow_led.value(0)
    
# Function for turning on green light, indicating that a connection was successful 
def green_light():
    #print("🟢 Green light on.")
    green_led.value(1)
    red_led.value(0)
    blue_led.value(0)
    yellow_led.value(0)
    
   
# Function for turning on red light, indicating that a connection has been shut down or is offline atm
def red_light():
    #print("🔴 Red light on.")
    red_led.value(1)
    blue_led.value(0)
    green_led.value(0)
    yellow_led.value(0)
    
    
# Function for flashing blue light, indicating a connection attempt
def blue_blink():
    #print("🔵 Blue light blinking.")
    #shut off all other LEDS when blinking blue light
    yellow_led.value(0)
    green_led.value(0)
    red_led.value(0)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)

# Function for blinking blue light without affecting other LEDS
def blue_blink2():
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    time.sleep(0.1)
    
# Function for blinking yellow light without sound 
def yellow_blink():
    yellow_led.value(1)
    time.sleep(0.1)
    yellow_led.value(0)
    time.sleep(0.1)
    yellow_led.value(1)
    time.sleep(0.1)
    yellow_led.value(0)
    time.sleep(0.1)
    yellow_led.value(1)
    time.sleep(0.1)
    yellow_led.value(0)
    time.sleep(0.1)

# Function for blinking red light without sound
def red_blink():
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    time.sleep(0.1)
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    time.sleep(0.1)
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    time.sleep(0.1)
    
        
# Function to turn on yellow flashing light to indicate errors occurd when trying to connect to Wi-Fi, LCD, RFID reader etc or invalid input
def yellow_light():
    yellow_led.value(1)
    beep(duration=0.5, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    for blink in range(5): # blink yellow light 5 times after the 
        yellow_led.value(0)
        time.sleep(0.2)
        yellow_led.value(1)
        time.sleep(0.2)
    yellow_led.value(0)
     
#---------------------------------------------------------------------------------------------------------
# Initialize and configure the LCD
# Create I2C-instance on GP4 (SDA) and GP5 (SCL)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)

# LCD-adress (my adress of the LCD: 0x27)
LCD_ADDR = 0x27

# Declaring som basic-functions for the LCD
def lcd_send_byte(data, mode):
    """ Send data to LCD via I2C. mode=0 for command, mode=1 for text """
    control = mode | 0x08  # Aktivera bakgrundsbelysning
    high_nibble = data & 0xF0
    low_nibble = (data << 4) & 0xF0
    i2c.writeto(LCD_ADDR, bytes([high_nibble | control, high_nibble | control | 0x04, high_nibble | control]))  # Send high nibble
    i2c.writeto(LCD_ADDR, bytes([low_nibble | control, low_nibble | control | 0x04, low_nibble | control]))  # Send low nibble

def lcd_init():
    """ Initiate LCD """
    time.sleep(0.02)  # standby for 20ms after startup
    lcd_send_byte(0x33, 0)  # Initiate-phase
    lcd_send_byte(0x32, 0)  # Switch to 4-byte mode
    lcd_send_byte(0x28, 0)  # 4-bite, 2 lines, 5x8 font
    lcd_send_byte(0x0C, 0)  # Display ON, Cursor OFF
    lcd_send_byte(0x06, 0)  # Move cursor to the right after displaying text
    lcd_send_byte(0x01, 0)  # Clear the screen
    time.sleep(0.002)

def lcd_write(text):
    """ Write text to LCD """
    for char in text:
        lcd_send_byte(ord(char), 1)  # Send character-by-character
def lcd_switch_line(col, row):
    """Move the cursor to a specific location"""
    pos = 0x80 + col + (0x40 * row)
    lcd_send_byte(pos, 0)
 
try:
    print("✅ LCD is turned on.")
    leds_on()
    lcd_init()
    leds_off()
    lcd_write("Power: ON")
    lcd_switch_line(0,1)
    lcd_write("LCD & LED:s...")
    leds_on()
    beep(duration=1, volume=13000, frequency=1832)
    leds_off()
    lcd_init()
    lcd_write("LCD: Connected,")
    lcd_switch_line(0,1)
    lcd_write("displays text!.")
    leds_on()
    time.sleep(0.1)
    leds_off()
    beep(duration=0.1, volume=15000, frequency=2500)
    leds_on()
    time.sleep(0.1)
    leds_off()
    beep(duration=0.1, volume=15000, frequency=2500)
    leds_on()
    time.sleep(1)
    leds_off()
    time.sleep(0.5)
    
except OSError:
    beep(duration=1, volume=15000, frequency=500)
    time.sleep(0.1)
    beep(duration=0.1, volume=12000, frequency=500)
    time.sleep(0.1)
    beep(duration=0.1, volume=12000, frequency=500)
    print("⚠️ LCD didn't startup correctly. Check jumperwires, power source to the Pico W and the I2C-configuration in Thonny.")
    lcd_init()
    lcd_write("LCD: error!")
    lcd_switch_line(0,1)
    lcd_write("check I2C-ports.")
    yellow_light()
    beep(duration=0.8, volume=15000, frequency=950)
    red_light()
    

#---------------------------------------------------------------------


# Configure SPI
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

# Creating Pin-object for CS and RST
cs_pin = Pin(17, Pin.OUT)
rst_pin = Pin(22, Pin.OUT)

# Initiate MFRC522 with SPI, CS och RST
rfid = MFRC522(spi, cs_pin, rst_pin)

# Identify the UID of the card and the tag

CARD_UID = [148, 195, 163, 219] 
TAG_UID = [65, 36, 32, 76]

# store them in the list of allowed tags

ALLOWED_TAGS = [
    [148, 195, 163, 219], [65, 36, 32, 76]
    ]

# Check first if the RFID reader is online
(status, _) = rfid.request(rfid.REQIDL)
if status != rfid.OK: # if pico W cant find or connect to the RFID
    print("❌ No RFID-reader found, check that the spi, cs_pin and rst_pin are configured correctly.")
    lcd_init()
    lcd_write(f"RFID: Offline.")
    lcd_switch_line(0,1)
    lcd_write("Check connections.")
    yellow_light()
    red_light()
    time.sleep(1)
else: 
    print(f"✅ RFID-reader is online and identified as {rfid}.")
    lcd_init()
    lcd_write("RFID: Online")
    lcd_switch_line(0,1)
    time.sleep(0.5)
    lcd_write(f"Model: MFRC522")
    beep(duration=0.1, volume=11000, frequency=1550)
    blue_led.value(1)
    time.sleep(0.1)
    blue_led.value(0)
    beep(duration=0.1, volume=13000, frequency=1750)
    red_led.value(1)
    time.sleep(0.1)
    red_led.value(0)
    yellow_led.value(1)
    beep(duration=0.5, volume=15000, frequency=1950)
    time.sleep(0.5)
    yellow_led.value(0)
    time.sleep(1)
    print("Scan a card or tag.")
    lcd_init()
    lcd_write("Scan card/tag")
    lcd_switch_line(0,1)
    lcd_write("...............")
    # Loop for tag detection
    while True:
        (status, tag_type) = rfid.request(rfid.REQIDL)  # Look for a tag
        if status == rfid.OK:# if a tag was found
            (status, uid) = rfid.anticoll() # try to read UID from the tag
            if status == rfid.OK and uid:# check if the tags UID was found
                uid_list = list(uid) # save the UID in the list of UID:s
                red_led.value(0)
                green_led.value(0)
                print("RFID-tag was scanned!, reading its UID...")
                lcd_init()
                lcd_write(f"RFID: Scanned!")
                lcd_switch_line(0,1)
                beep(duration=0.1, volume=15000, frequency=3250)
                time.sleep(0.1)
                beep(duration=0.1, volume=15000, frequency=3250)
                blue_blink()
                time.sleep(0.5)
                lcd_write("reading UID.....")
                time.sleep(0.5)
                print(f"✅ UID = {uid}")
                lcd_init()
                lcd_write("Identified UID:")
                lcd_switch_line(0,1)
                lcd_write(f"{uid}")
                time.sleep(1)
                if uid_list == ALLOWED_TAGS:
                #if uid_list == TAG_UID or uid_list == CARD_UID:
                    print("✅ UID was recognized from the list of tags.")
                    green_led.value(1)
                    lcd_init()
                    lcd_write(f"RFID: APPROVED")
                    lcd_switch_line(0,1)
                    lcd_write("status: UNLOCKED")
                    beep(duration=0.1, volume=15000, frequency=2050)
                    time.sleep(0.1)
                    beep(duration=0.3, volume=15000, frequency=3050)
                    time.sleep(1)
                    break
                else:
                    print("❌ Not approved, try another one.")
                    lcd_init()
                    lcd_write(f"RFID: DENIED")
                    lcd_switch_line(0,1)
                    lcd_write("status: LOCKED")
                    yellow_light()
                    time.sleep(0.5)
                    red_light()
                    lcd_init()
                    lcd_write(f"not recognized.")
                    lcd_switch_line(0,1)
                    lcd_write("Try another tag.")