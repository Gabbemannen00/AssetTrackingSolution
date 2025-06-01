from flask import Flask, request, jsonify
import sqlite3
import logging
import os

# Configure the path to the databasefile
DB_FILE = "/home/pi/RnD/Gabbemannen00/pi_zero/db/data.db"

# Configure logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s %(message)s]",

)

# Startlogg
logging.info(f"Using database file: {DB_FILE}")
print(f"🔍 Using database file: {DB_FILE}")

app = Flask(__name__)

def store_data(rfid_uid, event_type, value, timestamp):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rfid_data (rfid_uid, event_type, value, timestamp) VALUES (?, ?, ?, ?)",
            (rfid_uid, event_type, value, timestamp)
        )
        conn.commit()
        conn.close()
        msg = f"✅ Data stored: {rfid_uid}, {event_type}, {value}, {timestamp}"
        print(msg)
        logging.info(msg)
    except Exception as e:
        err = f"❌ Database error: {e}"
        print(err)
        logging.error(err)

# 🌐 Test-endpoint
@app.route("/")
def home():
    logging.info("Home endpoint accessed.")
    return "RFID Flask-Server is online."

# 📥 POST_endpoint for receiving and store data 
@app.route("/store", methods=["POST"])
def store():
    data = request.get_json()
    if "rfid_uid" in data and "event_type" in data and "value" in data and "timestamp" in data:
        try: 
            rfid_uid = data["rfid_uid"]
            event_type  = data["event_type"]
            value = float(data["value"]) 
            timestamp = data["timestamp"] 
            store_data(rfid_uid, event_type, value, timestamp)
            msg = f"📬 POST received and stored: {rfid_uid}, {event_type}, {value}, {timestamp}"
            print(msg)
            logging.info(msg)
            return jsonify({"message": "Data was stored successfully!"}), 201
        except ValueError:
            err = "⚠️  sensor_value must be a number."
            print(err)
            logging.warning(err)
            return jsonify({"error": err}), 400 
        except Exception as e:
            err = f"❌ Error processing request: {e}"
            print(err)
            logging.error(err)
            return jsonify({"error": "Internal error"}), 500
    else:
        err = "⚠️  Missing: 'rfid_uid' or 'event_type' or 'value' or 'timestamp'"
        print(err)
        logging.warning(err)
        return jsonify({"error": err}), 400

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
        logging.info("✅ Data retrieved successfully.")
        return jsonify(data), 200

    except Exception as e:
        err = f"❌ Error fetching data: {e}"
        print(err)
        logging.error(err)
        return jsonify({"error":"Internal error while fetching data"}), 500


if __name__ == "__main__":
    init = "🚀 Launching Flask..."
    logging.info(init)
    print(init)
    app.run(host="0.0.0.0", port=5000, debug=False)
  
