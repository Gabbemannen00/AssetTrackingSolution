import time # Import time module for delays
import machine # Import machine module for hardware control

# LCD command and control constants
LCD_CLEARDISPLAY = 0x01 # Clear the display and reset cursor
LCD_RETURNHOME = 0x02 # Return the cursor to the home position
LCD_ENTRYMODESET = 0x04 # Set the text entry mode
LCD_DISPLAYCONTROL = 0x08 # Control display, cursor, and blink settings
LCD_CURSORSHIFT = 0x10 # Move the cursor or shift the display
LCD_FUNCTIONSET = 0x20 # Set LCD function modes (data length, number of lines, font size)
LCD_SETCGRAMADDR = 0x40 # Set the CGRAM (character generator RAM) address
LCD_SETDDRAMADDR = 0x80 # Set the DDRAM (display data RAM) adress

# Flags for display control
LCD_DISPLAYON = 0x04 # Turn on the display
LCD_DISPLAYOFF = 0x00 # Turn off the display
LCD_CURSORON = 0x02 # Turn on the cursor
LCD_CURSOROFF = 0x00 # Turn of the cursor
LCD_BLINKON = 0x01 # Turn on blinking cursor
LCD_BLINKOFF = 0x00 # Turn of blinking cursor

# Flags for function set
LCD_8BITMODE = 0x10 # Use 8-bit data length
LCD_4BITMODE = 0x00 # Use 4-bit data length
LCD_2LINE = 0x08 # Use 2 lines
LCD_1LINE = 0x00 # Use 1 line
LCD_5x8DOTS = 0x00 # Use 5x8 dot front

#Flags for backlight control
LCD_BACKLIGHT = 0x08 # Turn on the backlight
LCD_NOBACKLIGHT = 0x00 # Turn off the backlight

# configure a class named I2cLcd with functions
class I2cLcd:
    def __init__(self, i2c, addr, num_lines, num_columns):
        """
        Initialize the LCD with the given I2c adress and display size.
        
        Parameters:
        - i2c (machine.I2C): The I2c bus object.
        - addr (int): The I2c address of the LCD module.
        - num_lines (int): The number of display lines (usally 2).
        - num_columns (int): The number of columns per line (typically 16).
        """
        self.i2c = i2c
        self.addr = addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = LCD_BACKLIGHT # Turn on backlight by dfault
        self.display_control = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF # Default display settings
        self.init_lcd() # Run the LCD initialization sequence

    def write_byte(self, data):
        """
        Send one byte to the LCD, including the backlight status.
        
        Parameters:
        - data (int): The byte to send to the LCD (8 bits).
        """
        try:
            self.i2c.writeto(self.addr, bytearray([data | self.backlight]))  # Skickar data med bakgrundsbelysning
        except Exception as e:
            print(f"Error in I2C communication: {e}")

    def send(self, data, mode):
        """
        Send 8-bit data to the LCD on4-bit mode (both low and high nibbles, high nibble first).
        
        Parameters:
        - data (int): The 8-bit data to send.
        - mode (int): The mode for the data (0 = command, 1 = character).
        """
        highnib = data & 0xF0 # Extract
        lownib = (data << 4) & 0xF0 #
        self.write_byte(highnib | mode) #
        self.toggle_enable(highnib | mode) #
        self.write_byte(lownib | mode) #
        self.toggle_enable(lownib | mode) #

    def toggle_enable(self, data):
        """
        
        """
        self.write_byte(data | 0x04)
        time.sleep_ms(1)
        self.write_byte(data & ~0x04)
        time.sleep_ms(1)

    def command(self, cmd):
        """Skicka ett kommando till LCD:n."""
        self.send(cmd, 0)

    def write(self, char):
        """Skicka ett tecken till LCD:n."""
        self.send(char, 1)

    def clear(self):
        """Rensa LCD-displayen."""
        self.command(LCD_CLEARDISPLAY)
        time.sleep_ms(2)

    def putstr(self, string):
        """Skriver en sträng på LCD:n."""
        for char in string:
            self.write(ord(char))

    def move_to(self, col, row):
        """Flytta markören till en viss position på LCD:n."""
        pos = col + (0x80 if row == 0 else 0xC0)  # 0x80 för rad 0, 0xC0 för rad 1
        self.command(pos)

    def init_lcd(self):
        """Initiera LCD:n i 4-bitars läge."""
        time.sleep_ms(100)  # Fördröjning för att säkerställa korrekt initiering
        self.command(LCD_FUNCTIONSET | LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS)
        time.sleep_ms(5)
        self.command(LCD_DISPLAYCONTROL | self.display_control)
        time.sleep_ms(5)
        self.clear()
        time.sleep_ms(5)
        self.command(LCD_ENTRYMODESET | 0x02)  # Sätt vänster till höger skrivning

    def backlight_on(self):
        """Slå på bakgrundsbelysningen."""
        self.backlight = LCD_BACKLIGHT
        self.write_byte(0)  # Kommando för att slå på bakgrundsbelysningen

    def backlight_off(self):
        """Slå av bakgrundsbelysningen."""
        self.backlight = LCD_NOBACKLIGHT
        self.write_byte(0)  # Kommando för att slå av bakgrundsbelysningen


