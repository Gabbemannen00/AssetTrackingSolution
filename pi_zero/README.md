# pi_zero

This folder contains the code running on the Raspberry Pi Zero 2 W, 
serving as the backend server and client for collecting data from RFID 
readers and sensors.

## Contents

- **db/** – Database files (e.g., `data.db`) storing collected sensor and 
RFID data.
- **flask-sqlite-server/** – A simple Flask application with SQLite to 
receive and store incoming data via HTTP.
- **scripts/** – Client scripts to send data to the server, such as from 
RFID readers or other sensors.
- **testing/** – Test code and temporary database experiments, e.g., 
`store_data.py` for testing sensor data collection.

