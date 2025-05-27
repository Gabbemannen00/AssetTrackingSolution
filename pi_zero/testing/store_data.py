import sqlite3
from datetime import datetime
import random

# create/open databasefile
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    temperature REAL,
    humidity REAL
)
''')

timestamp = datetime.now().isoformat()
temperature = round(random.uniform(20.0, 25.0), 2)
humidity = round(random.uniform(30.0, 50.0), 2)

# generate testdata

cursor.execute('''
INSERT INTO sensor_data (timestamp, temperature, humidity)
VALUES (?, ?, ?)
''', (timestamp, temperature, humidity))

conn.commit()
conn.close()

print(f"✔️ Saved line: {timestamp}, {temperature}°C, {humidity}% RH")
