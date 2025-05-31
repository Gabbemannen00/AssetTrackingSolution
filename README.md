# 📦 Asset Tracking Solution

This project is an **IoT-based asset tracking system** designed to monitor tagged items in short-term rental apartments. It uses a Raspberry Pi Pico W as the sensor unit to read RFID tags and a Raspberry Pi Zero 2 W as a server unit that stores and serves data over a local network.

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
  * IRQ (Optionally), was never used.
    
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
| **RFID Tags**       | Passive RFID key fobs and stickers              | —                                              |
| **LCD Display**     | 1602 LCD with I2C backpack                      | —                                              |
| **LEDs**            | Red, Green, Blue, Yellow *(connected to GPIOs)* | —                                              |
| **Button**          | Mounted on the breadboard to start main.py      | —                                              |
| **Buzzer**          | Connected via GPIO for audible alerts           | —                                              |
| **Wi-Fi**           | Built-in *(used for TCP/IP communication)*      | Built-in *(used to host Flask server)*         |
| **Power Source**    | USB from laptop or power bank                   | USB *(5V adapter or laptop)*                   |
| **Storage**         | Limited Storage, but can be extended            | MicroSD card(for data storage)                 |

> 📝 The **Pico W** is the sensor + client unit, reading RFID tags and sending data via TCP.
> 🧠 The **Pi Zero 2 W** acts as the backend server, storing data and exposing API endpoints via Flask.

## 📌 Data Flow Diagram

![asset_tracking_flow_diagram](https://github.com/user-attachments/assets/5270d074-6f8c-478e-94d5-65165c44e0ae)


## 📸 Hardware Images

*(Adding hardware setup images here for visual reference.*

```




``` 
## 📌 Notes

* No active tag-scanning was implemented, and no UHF antenna was used.
* Passive RFID tags are read directly from the MFRC522 reader mounted on the breadboard.
* Mesh networking and handheld RFID readers were not used in this prototype.
* This project is still under development—there are still many ways to develop the code and add hardware components to make the system more robust and powerful.
---

Feel free to explore the `pi_zero/` and `pico_w/` folders for full code and hardware setup details.
