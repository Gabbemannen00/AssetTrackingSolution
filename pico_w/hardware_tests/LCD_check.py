from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time
from time import sleep

# Använd GP4 & GP5 för standard I2C0, eller GP0 & GP1 för I2C1
I2C_SDA = Pin(4)  
I2C_SCL = Pin(5)  
i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=100000)  

# Leta efter I2C-enheter
i2c_addresses = i2c.scan()
print(f"Found I2C devices at addresses: {[hex(address) for address in i2c_addresses]}")

if not i2c_addresses:
    print("🚫 No I2C-device was found")
else:
    print(f"✅ I2C-devices found at addresses: {', '.join(hex(addr) for addr in i2c_addresses)}")
    lcd = I2cLcd(i2c, 0x27, 2, 16)  # LCD med adress 0x27

    time.sleep(3)

    print("A message will now be displayed on the LCD if it has been set up correctly.")

    lcd.clear()  # Rensa skärmen först
    time.sleep(1)
    print("First message is displayed.")
    lcd.putstr("Hello Gabriel!.")
    lcd.move_to(0,1)
    lcd.putstr("I'm your LCD,(=.")
    time.sleep(3)  # Ge tid att läsa
    print("Screen cleared.")
    lcd.clear()
    time.sleep(3)
    
    print("Displaying second message...")
    
    time.sleep(3)
    
    print("Second message is displayed.")
    lcd.putstr("I feel groggy.")
    lcd.move_to(0,1)
    lcd.putstr("I need to reboot.")
    time.sleep(3)
    print("Screen cleared.")
    lcd.clear()
    time.sleep(3)

    print("🔄 Restarting LCD...")

    lcd.backlight_off()  # Stäng av bakgrundsbelysning
    lcd.clear()
    print("🔴 LCD: turned off")
    
    time.sleep(3)
    
    lcd.backlight_on()  # Sätt på bakgrundsbelysning
    lcd.clear()
    print("🟢 LCD: Turned on")
    
    time.sleep(3)
    
    lcd.putstr("LCD:Connected to")
    lcd.move_to(0,1)
    lcd.putstr("RSB Pi Pico W.")
    
    print("✅ Your LCD and your Pico W are now connected (=")
