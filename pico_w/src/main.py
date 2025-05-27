import network 
import time
import utime
import socket
import urequests
from machine import Pin, SPI, I2C, PWM 
from MFRC522 import MFRC522
from time import localtime

#--------------------------------------------------------------------------------------------
# configure the button
button = Pin(7, Pin.IN, Pin.PULL_DOWN) # connected to GP9

#--------------------------------------------------------------------------------------------

 # configure buzzer (connect the buzzers (+) to pico GP16 and (-) to GND)
buzzer = PWM(Pin(16))

# Declaring a function for changing the sound of the buzzer. The sound can
# be modified by changing the duration, volume or frequency whenever it fits you
    
def beep(duration=0.1, volume=20000, frequency=4000):
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
    for _ in range(2):
        blue_led.value(1)
        time.sleep(0.1)
        blue_led.value(0)
        time.sleep(0.1)


# Function for blinking blue light without affecting other LEDS
def blue_blink2():
    for _ in range(3):
        blue_led.value(1)
        time.sleep(0.1)
        blue_led.value(0)
        time.sleep(0.1)
    
# Function for blinking yellow light without sound 
def yellow_blink():
    for _ in range(3):
        yellow_led.value(1)
        time.sleep(0.1)
        yellow_led.value(0)
        time.sleep(0.1)
   
# Function for blinking red light without sound
def red_blink():
    for _ in range(3):
        red_led.value(1)
        time.sleep(0.1)
        red_led.value(0)
        time.sleep(0.1)
    
# Function to turn on yellow flashing light to indicate errors occurd when trying to connect to Wi-Fi, LCD, RFID reader etc or invalid input
def yellow_light():
    yellow_led.value(1)
    beep(duration=0.5, volume=20000, frequency=950)
    time.sleep(0.1)
    for _ in range(3):
        beep(duration=0.1, volume=20000, frequency=950)
        time.sleep(0.1)
    for _ in range(5): # blink yellow light 5 times after the 
        yellow_led.value(0)
        time.sleep(0.2)
        yellow_led.value(1)
        time.sleep(0.2)
    yellow_led.value(0)
    
#---------------------------------------------------------------------------------------------------------
# My own design of sounds, lcd displays and lighting of LED:s

def tag_scanned_sound():
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

def TCP_connecting_sound():
    print("⏳ Starting up TCP...")
    lcd_init()
    lcd_write("Starting Server,")
    lcd_switch_line(0,1)
    lcd_write("standby...")
    time.sleep(1)
    for _ in range(3):
        blue_led.value(1)
        red_led.value(1)
        beep(duration=1, volume=15000, frequency=1250)
        yellow_blink()
        time.sleep(0.3)
        blue_led.value(0)
        red_led.value(0)
        time.sleep(0.3)
        
    leds = [Pin(14, Pin.OUT),
            Pin(13, Pin.OUT),
            Pin(15, Pin.OUT),
            Pin(8, Pin.OUT)
    ]
    for _ in range(5):
        for led in leds:
            led.value(1)
            time.sleep(0.1)
            led.value(0)
            time.sleep(0.1)
                
def TCP_restarting_leds():
    
    leds = [Pin(14, Pin.OUT),
            Pin(13, Pin.OUT),
            Pin(15, Pin.OUT),
            Pin(8, Pin.OUT)
    ]
    for _ in range(5):
        for led in leds:
            led.value(1)
            time.sleep(0.1)
            led.value(0)
            time.sleep(0.1)
    

        
        
#---------------------------------------------------------------------------------------------------------
# Initialize and configure the LCD
# Create I2C-instance on GP4 (SDA) and GP5 (SCL)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)

# LCD-adress (my adress of the LCD: 0x27)
LCD_ADDR = 0x27

# Declaring som basic-functions for the LCD
def lcd_send_byte(data, mode):
    """ Send data to LCD via I2C. mode=0 for command, mode=1 for text """
    control = mode | 0x08  # activate backlight
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
    
print("press the button")
lcd_init()
lcd_write("Press button to")
lcd_switch_line(0,1)
lcd_write("start the system.")

while True:
    if button.value() == 1:
        print("button pressed")
        break
    

try:
    print("✅ LCD is turned on.")
    leds_on()
    lcd_init()
    lcd_write("Power: ON")
    lcd_switch_line(0,1)
    beep(duration=1, volume=15000, frequency=2052)
    leds_off()
    beep(duration=0.2, volume=12000, frequency=1352)
    beep(duration=0.2, volume=13000, frequency=1522)
    beep(duration=0.3, volume=14000, frequency=1722)
    time.sleep(0.1)
    lcd_write("LCD: Online")
    leds_on()
    time.sleep(1)
    lcd_init()
    lcd_write("Welcome to JATS!")
    lcd_switch_line(0,1)
    lcd_write("smarter tracking")
    tones = [
        (1832, 0.1), # frequency and duration 
        (2500, 0.1),
        (2500, 0.3)
    ]
    for freq, duration in tones:
        leds_off()
        time.sleep(0.1)
        leds_on()
        beep(duration=duration , volume=15000, frequency=freq)
    

    time.sleep(3)
    leds_off()
    time.sleep(1)
    
except OSError:
    leds_off()
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
    
#--------------------------------------------------------------------------------------------------------------------------------
# Declaringa function that will send data to the Flask-server on Pi Zero via HTTP POST
# Used for sending RFID-tag and sensordata in JSON-format
# The flask server on Pi Zero needs to be online 24/7 for listening on the store endpoint
def send_to_flask_server(rfid_tag, sensor_value):
    try:
        
        # create timestamp
        t = localtime()
        formatted_time = f"{t[0]:04}-{t[1]:02}-{t[2]:02} {t[3]:02}:{t[4]:02}:{t[5]:02}"
        
        url = "http://raspberrypi.local:5000/store" # adress and port of the flask-server
        payload = {
            "rfid_tag": rfid_tag,
            "sensor_value": sensor_value,
            "timestamp": formatted_time
        }
        headers = {"Content-Type": "application/json"}
        
        response = urequests.post(url, json=payload, headers=headers)
        print("✅ Flask response: ", response.text)
        response.close()
    except Exception as e:
        print(f"❌ Error sending to Flask server: {e}")
#--------------------------------------------------------------------------------------------------------------------------------

# Configure your wifi information
SSID = ""
PASSWORD = ""

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
        lcd_write(f"Wi-Fi is") 
        lcd_switch_line(0,1)
        lcd_write("already online.")
        green_light()
        beep(duration=0.1, volume=15000, frequency=1750)
        time.sleep(0.1)
        beep(duration=0.1, volume=17000, frequency=1950)
        time.sleep(0.1)
        beep(duration=0.1, volume=19000, frequency=2150)
        return
    else: #run this code if Wi-Fi is not already connected
        wlan.connect(SSID, PASSWORD) #Try to connect 
        print("🔌🔄 Wi-Fi is offline.")
        lcd_init()
        lcd_write("Connecting to")
        lcd_switch_line(0,1)
        lcd_write("your wifi....") 
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
                lcd_write(f"Wi-Fi was") 
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
        lcd_write("your wifi...") 
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
            for _ in range(2):
                green_led.value(1)
                time.sleep(0.1)
                green_led.value(0)
                time.sleep(0.1)
            green_light()
            beep(duration=0.3, volume=15500, frequency=1250)
            time.sleep(0.1)
            beep(duration=0.5, volume=17000, frequency=1550)
            lcd_init()
            lcd_write(f"Wi-Fi: is now") 
            lcd_switch_line(0,1)
            lcd_write("reconnected.")
            time.sleep(1)
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
    lcd_write("to your wifi") 
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

# wait 1 second before try to connect to MFRC522
time.sleep(1)

#-------------------------------------------------------------------------------------------------------------------------------------

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
    print("To start the TCP_server you need to scan your card/tag.")
    lcd_init()
    lcd_write("Scan card/tag to")
    lcd_switch_line(0,1)
    lcd_write("start TCP_server")
    # Loop for tag detection
    while True:
        (status, tag_type) = rfid.request(rfid.REQIDL)  # Look for a tag
        time.sleep(0.05)
        if status == rfid.OK:# if a tag was found
            (status, uid) = rfid.anticoll() # try to read UID from the tag
            if status == rfid.OK and uid:# check if the tags UID was found
                uid_list = list(uid) # save the UID in the list of UID:s
                tag_scanned_sound()
                if uid_list == TAG_UID or uid_list == CARD_UID:
                    print("✅ UID was recognized from the list of tags.")
                    
                    # Send the tags UID to the flask server
                    uid_str = "-".join(str(byte)for byte in uid_list)
                    sensor_value = 0
                    send_to_flask_server(uid_str, sensor_value)
                    
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
                    
                    uid_str = "-".join(str(byte) for byte in uid_list)
                    sensor_value = -1 # Negative value send to Flask
                    send_to_flask_server(uid_str, sensor_value)
                    
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
             
#-----------------------------------------------------------------------------------------------------------------------------
#Create a TCP-server
# Serverconfiguration
SERVER_IP = wlan.ifconfig()[0] # Uses Pico W:s current IP:adress
SERVER_PORT = 5000 # Portnumber of Server
BUFFER_SIZE = 1024 # Max amount of data to recieve in bytes in each receivement

TCP_connecting_sound()

def handle_client(client_socket, client_adress):
    try:
        green_led.value(0)
        print(f"✅ connection from client adress: {client_adress}")
        for _ in range(3):
            lcd_init()
            lcd_write("Client connected!")
            lcd_switch_line(0,1)
            lcd_write(f"{client_adress}")
            yellow_led.value(1)
            red_led.value(1)
            blue_led.value(1)
            beep(duration=0.1, volume=15000, frequency=3050)
            yellow_led.value(0)
            red_led.value(0)
            blue_led.value(0)
        green_led.value(1)
        time.sleep(0.5)
        
        while True:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE)
            # check if no data was received
            if not data:
                print("No more messages received from Pi Zero.")
                for _ in range(3):
                    red_led.value(1)
                    lcd_init()
                    lcd_write("TCP: No more")
                    lcd_switch_line(0,1)
                    lcd_write("data received.)=")
                    beep(duration=0.5, volume=15000, frequency=1555)
                    red_led.value(0)
                    time.sleep(0.5)
                break # exit the loop when client is disconnected
            # Decode the received bytes to a string
            received_message = data.decode()
            for led, freq in zip([yellow_led, red_led, blue_led], [3555, 3555, 3555]):
                led.value(1)
                lcd_init()
                lcd_write("TCP: decoding")
                lcd_switch_line(0,1)
                lcd_write("byte to string...")
                beep(duration=0.3, volume=15000, frequency=freq)
                led.value(0)
                time.sleep(0.1)
            # When the message is decoded, send it to the Flask-server
            try:
                rfid_tag, sensor_value = received_message.split(",")
                sensor_value = float(sensor_value)
                send_to_flask_server(rfid_tag, sensor_value, formatted_time)
            except ValueError:
                print("⚠️ Incorrect format! Expected 'rfid_tag, sensor_value'")
            except Exception as e:
                print("⚠️ Failed to parse or send data to Flask: ",e)
            # print the received message in the terminal
            print(f"Received data: {received_message}")
            lcd_init()
            lcd_write("Converted bytes:")
            lcd_switch_line(0,1)
            lcd_write(f"{received_message}")
            for _ in range(2):
                beep(duration=0.1, volume=15000, frequency=3555)
                yellow_led.value(1)
                red_led.value(1)
                blue_led.value(1)
                time.sleep(0.1)
                yellow_led.value(0)
                red_led.value(0)
                blue_led.value(0)
            time.sleep(1.5) # Show the message for a little while
            # Send the same message back to the client (echo)
            client_socket.send(received_message.encode())
            print(f"Echoed back: {received_message}")
            lcd_init()
            lcd_write("TCP: Returned")
            lcd_switch_line(0,1)
            lcd_write("the message.")
            for led, freq in zip([blue_led, red_led, yellow_led],[1235, 1535, 1835]):
                led.value(1)
                beep(duration=0.1, volume=15000, frequency=freq)
                led.value(0)
                time.sleep(0.1)
            time.sleep(1.5) # wait a little before going back and receive more messages
                
    # Error during the communication with a connected client,
    # located inside the while true loop that handles the
    # client connection, from the line that accepts client adresses,
    # the while loop will look for another client until the error stops
    except Exception as e:
        print(f"⚠️ Error during communication: {e}")
        lcd_init()
        lcd_write("TCP:Error found!")
        lcd_switch_line(0,1)
        lcd_write("check logs.")
        yellow_blink()
        red_light()
                
    finally:
        # shut the connection to the client when everything is done
        print(f"🔌 Client {client_adress} disconnected.")
        client_socket.close()
        lcd_init()
        lcd_write("TCP: client")
        lcd_switch_line(0,1)
        lcd_write("got disconnected.")
        leds_on()
        beep(duration=0.3, volume=15000, frequency=1150)
        beep(duration=0.3, volume=15000, frequency=900)
        leds_off()
        time.sleep(1)
        lcd_init()
        lcd_write("TCP: restarting")
        lcd_switch_line(0,1)
        lcd_write("standby...")
        TCP_restarting_leds()

try: # Create a TCP-socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the given IP-adress and portnumber
    server_socket.bind((SERVER_IP, SERVER_PORT))
    # Start to listen for incomming connections(number 1 means accepting a connection)
    server_socket.listen(1)
    
    print(f"✅ TCP server is currently running on {SERVER_IP}:{SERVER_PORT}")
    lcd_init()
    lcd_write("TCP: Online")
    lcd_switch_line(0,1)
    lcd_write("Running 100%")
    green_led.value(1)
    beep(duration=0.1, volume=15000, frequency=2050)
    time.sleep(0.1)
    beep(duration=0.1, volume=15000, frequency=3050)
    time.sleep(1)
    lcd_init()
    lcd_write(f"IP: {SERVER_IP}")
    lcd_switch_line(0,1)
    lcd_write(f"PORT: {SERVER_PORT}")
    time.sleep(1)
    
    client_connections = 0
    
    while True:
        if client_connections > 0:
            green_led.value(1)
            print("TCP: restarted, start client on Pi Zero.")
            print("⏳ Waiting for a new connection...")
            lcd_init()
            lcd_write("TCP: restarted")
            lcd_switch_line(0,1)
            lcd_write("searching......")
            beep(duration=0.1, volume=15000, frequency=2050)
            time.sleep(0.1)
            beep(duration=0.1, volume=15000, frequency=3050)
        else:
            green_led.value(1)
            print("Now you can start the client on Pi Zero.")
            print("⏳ Waiting for a connection...")
            lcd_init()
            lcd_write("TCP: Waiting for")
            lcd_switch_line(0,1)
            lcd_write("a connnection.....")
            client_connections+=1
            
        try:
            client_socket, client_adress = server_socket.accept()
            # Try to find another client again by calling the function
            handle_client(client_socket, client_adress)
        # run except whenever there is a fault detected with the client connection
        except Exception as e:
            print(f"⚠️ Error accepting client: {e}")
            lcd_init()
            lcd_write("TCP: client error")
            lcd_switch_line(0,1)
            lcd_write("check logs.")
            yellow_blink()
            red_light()
                      
# Possible failures that can make this code block running:
# Error during server startup, located all around the startup,
# critical failures that can force the server to restart
except Exception as e:
    print(f"❌ Server error: {e}")
    lcd_init()
    lcd_write("TCP:Error found!")
    lcd_switch_line(0,1)
    lcd_write("during startup.")
    yellow_light()
    lcd_init()
    lcd_write("TCP:interrupted,")
    lcd_switch_line(0,1)
    lcd_write("fix the error!.")
    red_light()

    
           














