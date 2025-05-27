import time
import network
from machine import Pin, I2C, SPI, PWM

#--------------------------------------------------------------------------------------------

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
green_led = Pin(14, Pin.OUT)  # Green LED
red_led = Pin(15, Pin.OUT)    # Red LED
blue_led = Pin(13, Pin.OUT)   # Blue LED
yellow_led =Pin(8, Pin.OUT)   # Yellow LED

# Start the program always with the LED:s set to off
green_led.value(0)
red_led.value(0)
blue_led.value(0)
yellow_led.value(0)


# Function for starting all the LED:s at once
def leds_on():
    for led in [green_led, red_led, blue_led, yellow_led]:
        led.value(1)
    
# Function for shutting off all the LED:s at once
def leds_off():
    for led in [green_led, red_led, blue_led, yellow_led]:
        led.value(0)
    
# Function for turning on green light, indicating that a connection was successful 
def green_light():
    #print("🟢 Green light on.")
    leds_off()
    green_led.value(1)
    
# Function for turning on red light, indicating that a connection has been shut down or is offline atm
def red_light():
    #print("🔴 Red light on.")
    leds_off()
    red_led.value(1)
     
# Function for turning on flashing blue light, indicating a connection attempt
def blue_blink():
    #print("🔵 Blue light blinking.")
    leds_off()
    for _ in range(2):
        blue_led.value(1)
        time.sleep(0.1)
        blue_led.value(0)
        time.sleep(0.1)
    
# Function to turn on yellow flashing light to indicate errors occurd when trying to connect to Wi-Fi, LCD, RFID reader etc or invalid input
def yellow_light():
    #print("Yellow light slow blinking.")
    leds_off()
    yellow_led.value(1)
    beep(duration=0.5, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    time.sleep(0.1)
    beep(duration=0.1, volume=20000, frequency=950)
    for _ in range(5): # blink yellow light 5 times after the 
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
    control = mode | 0x08  # Activate the backlight
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
    lcd_write("LCD: Online")
    leds_on()
    beep(duration=0.1, volume=10000, frequency=2000)
    
    
    lcd_switch_line(0,1)
    leds_off()
    time.sleep(0.1)
    lcd_write("displaying text.")
    leds_on()
    beep(duration=0.1, volume=15000, frequency=3000)
    leds_off()
    time.sleep(0.1)
    leds_on()
    beep(duration=0.3, volume=10000, frequency=3000)
    time.sleep(2)
    leds_off()
    time.sleep(1)
    
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
    
#------------------------------------------------------------------------------------------

# Declaring Wi-Fi-information
SSID = "" # put your wifi username here
PASSWORD = "" # put your password here

# Creating Wi-Fi-object
wlan = network.WLAN(network.STA_IF)

#function for connecting automatically to Wi-fi and check if it's not already connected
def connect_wifi():
    """Automatically connects to Wi-Fi if not already connected."""
    wlan.active(True) #Wi-Fi on
    
    if wlan.isconnected():
        print("✅ Wi-Fi is already connected.")
        print(f"✅ Wi-Fi: {SSID}")
        lcd_init()
        lcd_write(f"Wi-Fi:{SSID}")
        lcd_switch_line(0,1)
        lcd_write("already online!.")
        green_light()
        beep(duration=0.1, volume=15000, frequency=1750)
        time.sleep(0.1)
        beep(duration=0.1, volume=17000, frequency=1950)
        time.sleep(0.1)
        beep(duration=0.1, volume=19000, frequency=2150)
        time.sleep(1)
        return
    else: 
        wlan.connect(SSID, PASSWORD) #Try to connect 
        print("🔌🔄 Wi-Fi is offline.")
        lcd_init()
        lcd_write("Connecting to")
        lcd_switch_line(0,1)
        lcd_write(f"{SSID}......")
        print("⏳Trying to connect...")
        for i in range(10):# wait 10 seconds max
            if wlan.isconnected():
                if i <= 3:
                    print("🚀 Network responded fast.")
                elif i > 3 and i <= 6:
                    print("⏳ Network responded ok.")
                elif i > 6 and i < 10:
                    print("🐢 Network responded slow.")
                    
                print(f"✅ Connection successful! Took {i} seconds.")
                print(f"✅ Wi-Fi is connected to SSID: {SSID}")
                lcd_init()
                lcd_write(f"Wi-Fi:{SSID}")
                lcd_switch_line(0,1)
                lcd_write("auto-connected.")
                green_light()
                beep(duration=0.2, volume=15500, frequency=1250)
                time.sleep(0.1)
                beep(duration=0.5, volume=17000, frequency=1550)
                return True
            i=i+1
            print(f"Attempts: {i} ")
            blue_blink()
            beep(duration=0.1, volume=15000, frequency=1854)
            time.sleep(0.1)
            blue_blink()
            beep(duration=0.1, volume=15000, frequency=1854)
            time.sleep(1) #wait 1 second between each attempt to connect
        # After 10 attempts to connect, exit the for loop and inform the user that a connection was not successful and what the user can do about it
        print(f"❌ Failed to connect to Wi-Fi after 10 attempts with SSID: {SSID}")
        print("Check if the Wi-Fi-info contains incorrect symbols/numbers. Check your and make sure all cables and jumperwires are connected correctly. If nothing works, try restarting your devices, including your router.")
        lcd_init()
        lcd_write(f"No contact...")
        lcd_switch_line(0,1)
        lcd_write("Wi-Fi offline.")
        green_led.value(0)
        red_light()
        beep(duration=2, volume=15000, frequency=950)
        time.sleep(1)
        return False
    
#function for reconnecting to Wi-Fi 
def reconnect_wifi():
    wlan.connect(SSID, PASSWORD)  # Try to connect
    print(f"⏳ Reconnecting to: {SSID}....")
    for i in range(10):# wait 10 seconds max
        lcd_init()
        lcd_write("Reconnecting to")
        lcd_switch_line(0,1)
        lcd_write(f"{SSID}......")
        if wlan.isconnected():
            if i <= 3: #if it takes less than- or exactly 3 seconds to reconnect
                print("🚀 Network reconnected fast.")
            elif i > 3 and i <= 6: 
                print("⏳ Network reconnected ok.")
            elif i > 6 and i < 10:
                print("🐢 Network reconnected slow.")
                 
            print(f"✅ Reonnection successful! Took {i}/10 attempts.")
            print(f"✅ Reonnected to: {SSID}")
            lcd_init()
            lcd_write("Reconnection")
            lcd_switch_line(0,1)
            lcd_write("successful!.")
            green_led.value(1)
            time.sleep(0.1)
            green_led.value(0)
            time.sleep(0.1)
            green_led.value(1)
            time.sleep(0.1)
            green_led.value(0)
            time.sleep(0.1)
            green_light()
            beep(duration=0.3, volume=15500, frequency=1250)
            time.sleep(0.1)
            beep(duration=0.5, volume=17000, frequency=1550)
            time.sleep(0.1)
            return True
        blue_blink()
        beep(duration=0.1, volume=15000, frequency=1854)
        time.sleep(0.1)
        beep(duration=0.1, volume=15000, frequency=1854)
        i=i+1
        print(f"Attempts: {i} ")
        time.sleep(1) #wait 1 second between each attempt to connect

    print(f"❌ Failed to reconnect to Wi-Fi after 10 seconds with SSID: {SSID}")
    print("Check if the Wi-Fi-info contains incorrect symbols/numbers. Check router and make sure cables are connected right. If nothing works, try restarting your devices, included your router.")
    lcd_init()
    lcd_write(f"Failed reconnect.")
    lcd_switch_line(0,1)
    lcd_write(f"Wi-Fi:{SSID}")
    beep(duration=0.8, volume=15000, frequency=950)
    time.sleep(1)
    return False

 # function for disconnecting Wi-Fi
def disconnect_wifi():
    """Koppla från Wi-Fi."""
    if wlan.isconnected():
        wlan.disconnect()
        print("🔌 Wi-Fi disconnected.")
        lcd_init()
        lcd_write(f"Wi-Fi:{SSID}")
        lcd_switch_line(0,1)
        lcd_write("got disconnected.")
        red_light()
        beep(duration=0.3, volume=15000, frequency=1150)
        beep(duration=0.3, volume=15000, frequency=900)
        
    else:
        print("⚠️ No Wi-Fi connection found to disconnect.")
        beep(duration=1, volume=15000, frequency=950)
        lcd_init()
        lcd_write("No Wi-Fi to")
        lcd_switch_line(0,1)
        lcd_write("disconnect from.")
        
        
# function for checking if Wi-Fi is active
def is_connected():
    """Return True if Wi-Fi is connected, otherwise return False."""
    return wlan.isconnected()
 
# 🚀 Connect Wi-Fi automatically at startup.

connect_wifi()

#-----------------------------------------------------------------------------------------------------------------------------------
#Wifi-manager code begins here

while True:
    if not is_connected(): #if wifi is offline and you want to try to connect
        lcd_init()
        lcd_write("Welcome to the")
        lcd_switch_line(0,1)
        lcd_write("wifi-manager!.")
        time.sleep(2)
        print("🔌🔄 Wi-Fi is offline.")
        lcd_init()
        lcd_write(f"Wi-Fi:{SSID}")
        lcd_switch_line(0,1)
        lcd_write("is not connected.")
        print("|----------------------|")
        print("|*-_-*Wifi-Manager*-_-*|")
        print("|----------------------|")
        connect = input("Try connect to Wi-Fi? (yes/no): ").strip().lower()
    
        if connect == "yes":
            reconnect_wifi() #initiate a reconnection 
            
        elif connect == "no":
             print("🔌❌ Wi-Fi will remain offline.")
             lcd_init()
             lcd_write("Wi-Fi: offline.")
             lcd_switch_line(0,1)
             lcd_write("Will remain off.")
             red_light()
             time.sleep(3)
             lcd_init()
             lcd_write(f"Wi-Fi:{SSID}")
             lcd_switch_line(0,1)
             lcd_write("is offline.")
             break
            
        else:
            print("⚠️ Invalid answer, try again.")
            red_light()
            lcd_init()
            lcd_write("Error: bad reply")
            lcd_switch_line(0,1)
            lcd_write(f"YourInput: {connect}")
            yellow_light()
            lcd_init()
            lcd_write(f"Wi-Fi:{SSID}")
            lcd_switch_line(0,1)
            lcd_write("is offline.")
            red_light()
            
            
    elif is_connected():#if Wi-Fi is connected but you want to disconnect and reconnect
        lcd_init()
        lcd_write("Welcome to the")
        lcd_switch_line(0,1)
        lcd_write("wifi-manager!.")
        time.sleep(2)
        lcd_init()
        lcd_write(f"Wi-Fi:{SSID}")
        lcd_switch_line(0,1)
        lcd_write("is connected.")
        print("|----------------------|")
        print("|*-_-*Wifi-Manager*-_-*|")
        print("|----------------------|")
        user_input = input("Disconnect Wi-Fi? (yes/no): ").strip().lower()
        if user_input == "yes":
            disconnect_wifi()
            
            # Asking the user if he/she wants to reconnect
            reconnect = input("Reconnect Wi-Fi? (yes/no): ").strip().lower()
            
            if reconnect == "yes":
                reconnect_wifi() #initiate a reconnection to Wi-fi
                
            elif reconnect == "no":
                print("🔌❌ Wi-Fi will remain offline until next startup.")
                lcd_init()
                lcd_write("Wi-Fi: offline.")
                lcd_switch_line(0,1)
                lcd_write("Will remain off.")
                red_light()
                time.sleep(3)
                lcd_init()
                lcd_write(f"Wi-Fi:{SSID}")
                lcd_switch_line(0,1)
                lcd_write("is offline.")
                break
            
            else:
                print("⚠️ Invalid answer, try again.")
                red_light()
                lcd_init()
                lcd_write("Error: bad reply")
                lcd_switch_line(0,1)
                lcd_write(f"YourInput: {reconnect}")
                yellow_light()
                lcd_init()
                lcd_write(f"Wi-Fi:{SSID}")
                lcd_switch_line(0,1)
                lcd_write("is offline.")
                red_light()
               
            
        elif user_input == "no":
            print("✅ Wi-Fi will stay connected.")
            lcd_init()
            lcd_write(f"Wi-Fi will")
            lcd_switch_line(0,1)
            lcd_write("stay connected.")
            green_light()
            time.sleep(3)
            lcd_init()
            lcd_write(f"Wi-Fi:{SSID}")
            lcd_switch_line(0,1)
            lcd_write("is connected!.(=")
            break  

        else: #disconnect invalid input
            print("⚠️ Invalid answer, try again.")
            green_light()
            lcd_init()
            lcd_write("Error: bad reply")
            lcd_switch_line(0,1)
            lcd_write(f"YourInput: {user_input}")
            yellow_light()
            #time.sleep(1)
            lcd_init()
            lcd_write(f"Wi-Fi:{SSID}")
            lcd_switch_line(0,1)
            lcd_write("is connected!.(=")
            green_light()
           
                      
        
        
