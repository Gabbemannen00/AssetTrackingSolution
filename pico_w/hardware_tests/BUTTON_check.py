import time
from machine import Pin

# configure the button
button = Pin(7, Pin.IN, Pin.PULL_DOWN) # connected to GP9

print("press the button")

while True:
    if button.value() == 1:
        print("button pressed")
        time.sleep(1)
