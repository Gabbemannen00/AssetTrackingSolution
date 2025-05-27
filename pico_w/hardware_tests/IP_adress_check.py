import network

wlan = network.WLAN(network.STA_IF)
print(wlan.ifconfig()) #This line returns a tuple with the IP-adress
