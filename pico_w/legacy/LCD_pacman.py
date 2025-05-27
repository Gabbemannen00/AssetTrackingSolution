from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time

I2C_SDA = Pin(4)  # Justera till din SDA-pin
I2C_SCL = Pin(5)  # Justera till din SCL-pin
i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=100000)  # 100kHz är tillräckligt för LCD

i2c_addresses = i2c.scan()
if not i2c_addresses:
    print("Ingen I2C-enhet hittades!")
else:
    print(f"I2C-enhet hittad på adress: {hex(i2c_addresses[0])}")
    lcd = I2cLcd(i2c, 0x27, 2, 16)  # Använd rätt adress (0x27 eller 0x3F)
    
    lcd.putstr(" O O O O O O O O")
    lcd.move_to(0,1)
    lcd.putstr(" 1 1 1 1 1 1 1  ")
    time.sleep(1)
    lcd.putstr("<O O O O O O O")
    lcd.move_to(0,1)
    lcd.putstr(" 1 1 1 1 1 1 1>")
    time.sleep(1)
    
    
    
 
    
    
    
