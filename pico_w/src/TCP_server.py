import time
import socket #import socket module in order to use TCP/IP communication
from machine import Pin, SPI, I2C, PWM
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

#---------------------------------------------------------------------

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
    
        
# Function to turn on yellow flashing light to indicate errors when trying to connect to Wi-Fi, LCD, RFID reader etc or invalid input
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

# Serverconfiguration
SERVER_IP = "192.168.1.128" # Pico W:s IP-adress (change if needed)
SERVER_PORT = 5000 # Portnumber of Server
BUFFER_SIZE = 1024 # Max amount of data to recieve in bytes in each receivement

# Create a TCP-socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow reuse of adress in order to avoid "Address already in use" after restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the given IP-adress and portnumber
server_socket.bind((SERVER_IP, SERVER_PORT))

# Start to listen for incomming connections(1 means we accept a connection)
server_socket.listen(1)

# track the amount of connections that has been done with client before
client_connections = 0

while True:
    # if a client connection has been done before
    if client_connections > 0:
        print("Looking for a new connection...")
        lcd_init()
        lcd_write("TCP: Restarted!")
        lcd_switch_line(0,1)
        lcd_write("searching again...")
    else:
        print("Looking for a first connection...")
        lcd_init()
        lcd_write("TCP: Searching")
        lcd_switch_line(0,1)
        lcd_write("for a client....")
        client_connections+=1 
        
    try:
        # Accept an incomming connection from client
        client_socket, client_adress = server_socket.accept()
        print(f"Connection from client adress: {client_adress}")
    
        # continue to receive messages until the client shuts the connection
        while True:
            # receive data from the client
            data = client_socket.recv(BUFFER_SIZE)
        
            # check if no data was received after the connection was shut down
            if not data:
                print("")
                print("No more data was received from client.")
                break # exit the loop when client is disconnected
        
            # Decode the received bytes to a string
            received_message = data.decode()
        
            # print the received message in the terminal
            print(f"From Pi Zero: {received_message}")
        
            # Send the same message back to the client (echo)
            client_socket.send(received_message.encode())
            print(f"Sent back: {received_message}")
            
     # handle unexpected failures during communication with client
    except Exception as e:
        print(f"Error: {e}")
    # shut the connection to the client when everything is done
    finally:
        client_socket.close()
        print("Connection closed.")
        print("")
