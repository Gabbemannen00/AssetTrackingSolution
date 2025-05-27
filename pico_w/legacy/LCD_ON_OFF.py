from machine import Pin,I2C
from i2c_lcd import I2cLcd # import library for running the lcd
import time
# 🛠️ configure I2C on GP0 (SDA) och GP1 (SCL)

I2C_SDA = Pin(4)  #  SDA-pin
I2C_SCL = Pin(5)  # SCL-pin

i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=100000)  # 100kHz är tillräckli

# 🔎 try to find the I2C-adress for the LCD
i2c_adresses = i2c.scan()
if not i2c_adresses: 
    print("❌ No I2C-device was found. Check the connections on your Pico!")
else:
    lcd_adress = i2c_adresses[0]
    lcd = I2cLcd(i2c, lcd_adress, 2, 16) # LCD 16x2
    
if i2c_adresses: #only if a LCD was found
    # 🔄 restart the LCD by turning it off, wait a couple of seconds and then turn it back on
    lcd.backlight_off()  # shuts off the LCD:s background light
    lcd.clear()          # clear the screen
    print("❌ LCD has been shut down.")
    print("🔄 Turning it back on in 5 seconds...")
    time.sleep(5)  # give the LCD 5 seconds to power up again
    
    lcd.backlight_on()  # turn it on again
    lcd.clear()
    lcd.putstr("LCD: ON")# display message on the LCD that confirms that it has been restarted
    print("✅ LCD has been turned on.")

