# 📦 Asset Tracking Solution

This project is an **IoT-based asset tracking system** designed to monitor RFID-tagged items in short-term rental apartments. It uses a Raspberry Pi Pico W as the sensor unit to read RFID tags and a Raspberry Pi Zero 2 W as a server unit that stores and serves data over a local network.

## 🧠 System Architecture

* **Raspberry Pi Pico W**: Reads passive RFID tags via an MFRC522 module and sends UID + timestamp data over TCP.
* **Raspberry Pi Zero 2 W**: Runs a Flask + SQLite backend to receive, store, and serve data from RFID scans.

## 📂 Project Structure

```
AssetTrackingSolution/
├── pi_zero/        # Backend server: Flask app + SQLite + test clients
└── pico_w/         # Sensor unit: RFID reading + LEDs + LCD + Wi-Fi TCP client
```

## 🔌 Wiring & Connections

### Raspberry Pi Pico W

* **MFRC522 RFID Reader**:

  * VCC → 3V3
  * GND → GND
  * RST → GP22 *(Reset signal)*
  * MOSI → GP11
  * MISO → GP12
  * SCK → GP10 *(SPI communication)*
  * SDA (NSS) → GP17 *(Chip Select)*
  * IRQ (Optionally), not used in this project.
    
* **LCD (1602 I2C)**:

  * SDA → GP4
  * SCL → GP5 *(I2C communication)*
  * VCC → VSYS (5V) # for power.
  * GND → GND
    
* **LED:s**:

  * GP14 → (Green)
  * GP15 → (Red)
  * GP13 → (Blue)
  * GP8 → (Yellow)
  
* **Buzzer**:
  
  GP16 *(via resistor, GND to ground)*
  
* **Button**:
  
  * GP7 → GND *(Makes the user able to start the system directly on the breadboard without having to login to the computer, open the editor and run the program.)*

### Raspberry Pi Zero 2 W

* Connected via Wi-Fi to the same network as the Pico W.
* Runs `app.py` which is the Flask server and listens for incoming RFID data.
* Connects to the SQLite database to store scan records.
* Connected with usb- to micro-usb cables .

## 🧰 Hardware Overview

| IoT-device:         | Raspberry Pi Pico W (Microcontroller)            | Raspberry Pi Zero 2 W (Single-board computer) |
| ------------------- | ----------------------------------------------- | ---------------------------------------------- |
| **RFID Reader**     | MFRC522 *(SPI connection)*                      | —                                              |
| **RFID Tags**       | Passive RFID-tags/cards                         | —                                              |
| **LCD Display**     | 1602 LCD with I2C backpack                      | —                                              |
| **LEDs**            | Red, Green, Blue, Yellow *(connected to GPIOs)* | —                                              |
| **Button**          | Mounted on the breadboard to start main.py      | —                                              |
| **Buzzer**          | Connected via GPIO for audible alerts           | —                                              |
| **Wi-Fi**           | Built-in *(used for TCP/IP communication)*      | Built-in *(used to host Flask server)*         |
| **Power Source**    | USB from laptop or power bank                   | USB *(5V adapter or laptop)*                   |
| **Storage**         | Limited Storage, but can be extended            | MicroSD card(for data storage)                 |

> 📝 The **Pico W** is the sensor + client unit, reading RFID tags and sending data via TCP to Pi Zero.
> 🧠 The **Pi Zero 2 W** acts as the backend server, storing data and exposing API endpoints via Flask.

## 📌 Data Flow Diagram

![asset_tracking_flow_diagram](https://github.com/user-attachments/assets/5270d074-6f8c-478e-94d5-65165c44e0ae)

## 📸 Hardware Images (for visual reference)

*(Raspberry Pi Pico hardware setup, including breadboard wiring with RFID-reader, LCD, LED:s and button)*

--

## Raspberry Pi Zero 2 W Setup 

### 1️⃣ All hardware parts needed: 
![All Components](https://github.com/user-attachments/assets/2efea73a-96c9-447a-9fa8-f855ad0cfb07)

1. Micro SD card with 32GB (with Raspberry Pi OS pre-installed)
2. Raspberry Pi Zero 2 W
3. Three different kinds of cover to the case
4. Raspberry Pi Zero case
5. USB 2.0 hub(4 ports)
6. Micro-USB male to USB female adapter
7. USB-cable A-male to Micro B-male
8. USB-cable male to male (1 meter)
9. HDMI-adapter (forgot to add it in the picture)

### 🪛 Installation step by step:

#### 2️⃣ Connect the USB male to male cable

![USB-male to male](https://github.com/user-attachments/assets/d4c6acb8-5489-43dd-a82c-7e162de0c216)

![Hub is powered](https://github.com/user-attachments/assets/e1b725a9-1f80-451e-a7d2-d18216bb3771)

By connecting this cable to the hub, the hub gets power directly from the pc, and all 4 ports become available for you to connect to Pi Zero.

#### Prepare your SD-Card with OS 

![SDcard mounted](https://github.com/user-attachments/assets/9536db2e-cf93-4380-a947-cb008998f3c6)

![Pi Zero placed in the case](https://github.com/user-attachments/assets/bb436b4c-ae57-41ef-a2e7-436fbb149fcf)

⚠️ Before you plug in the SD-card into Pi Zero, make sure you have a Raspberry Pi operativesystem pre-installed.

You can install any OS on https://www.raspberrypi.com/software/. Otherwise you are good to go and then place Pi Zero into the case.

The SD Card makes you able to start, run and store data on Pi Zero. The case is for protecting the device from scratches, fall damages, etc.

#### 3️⃣ Examine the ports of the case

![Ports](https://github.com/user-attachments/assets/70aaa33b-fc53-4198-bd8f-b7a6b7985dfb)

Here you can see three different kind of ports. 

The right port: micro-USB for power supply

The middle port: micro-USB for data transmissions via USB-OTG adapter.

The third port: mini-HDMI for connecting to a monitor.

#### 4️⃣ Connect the powercable (USB-male to micro-male)

![USB-male to Micro-male](https://github.com/user-attachments/assets/a33db2f9-85d8-453d-8cbf-87e33358a135)

![USB-male to micro-male connected](https://github.com/user-attachments/assets/2a90e9e2-0987-480f-bb3a-b86aabb0abb8)

Now you will see Pi Zero's light start to blink, its because its booting. When the blinking stops, the device is on.

#### 5️⃣ Prepare the OTG-adapter for data

![Micro-USB-male to USB-female adapter connected](https://github.com/user-attachments/assets/5ca2cf66-90fd-4107-ba21-c9613bc4ed1c)

You are going to need a micro-USB male to micro-USB female adapter for data transmissions to work properly. Make sure to connect the adapter's micro USB male to the middle port on Pi Zero and then plug the hub's USB cable to female.

#### 6️⃣ Connect screen (Optionally). Skip this? Go straight to step 7

![Holding HDMI-cable](https://github.com/user-attachments/assets/7feb6733-16f8-4475-85d5-d5e39de13c9a)

First you need an ordinary HDMI-cable which i assume that you already have. If not you need to buy one fast as f**k.

![Holding HDMI-female adapter to mini-HDMI-male](https://github.com/user-attachments/assets/c055f722-a4f8-4870-8196-7d58ffafbbd8)

Secondly you need a mini-HDMI male to HDMI female-adapter to power the interface of Pi Zero. 

![All cables connected to Pi Zero](https://github.com/user-attachments/assets/51c0dd06-8c40-4aae-888d-b97f4d008a9c)

And now everything is connected to Pi Zero, it now receives power, data transmissions and send screensignals to the monitor. Also dont forget to select the right HDMI-port on your screen, the one that your HDMI cable is connected to.

#### Finally connect mouse and keyboard 

![keyboard and mouse connected too](https://github.com/user-attachments/assets/ab84e5db-884a-47b2-b04e-abd761a163be)

Now there should be two available ports on the hub for you to connect your mouse and keyboard

![Monitor connected, logging in to Pi Zero](https://github.com/user-attachments/assets/b9a67264-f23c-413b-a14e-39ce5dc054be)

Now you can enter username "pi" and password "raspberry" to login to Pi Zero, you can change these later if you want.

#### Desktop of Pi Zero view

![Desktop of Pi Zero](https://github.com/user-attachments/assets/23ab44f6-4159-4d0e-ae0e-d0a66a0ac602)

Now you have full control over Raspberry Pi Zero 2 W and you can start using all its functionalities. 

#### 7️⃣ Connect Pi Zero (HEADLESS)

This is for you who dont want or not able to connect Pi Zero to screen, keyboard or mouse and instead want to access it directly from the computer. But first you're gonna have to make sure the SD-Card is setup properly, so you can connect via SSH. This is called a headless setup. 

Step 1: Make sure you have OS installed and configured like i told you before.

Step 2: Unplug the SD card from Pi Zero and plug it into the computer using it's case that it camed with or if you have an SD card module.

Step 3: When you see something like "bootfs", double click on it, look for a map called "boot", enter it and create an empty file (without extensions), name the file exactly: ssh  

Step 4: Add your Wifi-information by creating a file in the same map and name the file: wpa_supplicant.conf 

Step 5: In wpa_supplicant file you enter this code, and enter your actual username and password for your Wi-Fi: 

```
country=SE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YourWIFIusername"
    psk="YourPassword"
    key_mgmt=WPA-PSK
}
```

Step 6: Save and quit, unplug the SD-card from the computer and plug it in to Pi Zero. 

Step 7: In order to connect to your Pi Zero you need to open a terminal window and enter "ssh pi@<pi-adress>", when you know your ip-adress of your Pi Zero replace this part "<pi-adress>" to pi zero's ip-adress, so it looks something like this "ssh pi@191.156.2.159".

Step 8: Enter username "pi" and password "raspberry". Now you have logged in to your Pi Zero and can start coding, create and edit files.

---

## 📌 Notes

* No active tag-scanning was implemented, and no UHF antenna was used.
* Passive RFID tags are read directly from the MFRC522 reader mounted on the breadboard.
* Mesh networking and handheld RFID readers were not used in this prototype.
* This project is still under development—there are still many ways to develop the code and add hardware components to make the system more robust and powerful.
---

Feel free to explore the `pi_zero/` and `pico_w/` folders for full code and hardware setup details.
