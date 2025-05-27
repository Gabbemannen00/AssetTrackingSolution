from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)
DB_FILE = "data.db"

def store_data(rfid_tag, sensor_value, timestamp):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rfid_data (rfid_tag, sensor_value, timestamp) VALUES (?, ?, ?)",
            (rfid_tag, sensor_value, timestamp)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
 
@app.route("/")
def home():
    return "RFID Flask-Server is online."

@app.route("/store", methods=["POST"])
def store():
    data = request.get_json()
    if "rfid_tag" in data and "sensor_value" in data and "timestamp" in data:
        try: 
            rfid_tag = data["rfid_tag"]
            sensor_value = float(data["sensor_value"]) # Make sure it's right
            timestamp = data["timestamp"] 
            store_data(rfid_tag, sensor_value, timestamp)
            return jsonify({"message": "Data was stored successfully!"}), 201
        except ValueError:
            return jsonify({"error": "sensor_value must be a number."}), 400 
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return jsonify({"error": "Internal error"}), 500
    else:
        return jsonify({"error":"Missing 'rfid_tag' or 'sensor_value' or 'timestamp'"}), 400

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rfid_data ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        data = [dict(row) for row in rows]
        return jsonify(data), 200

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({"error":"Internal error while fetching data"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
  
