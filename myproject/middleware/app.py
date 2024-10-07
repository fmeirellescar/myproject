from services.sensor_handler import start_mqtt_listener
from flask import Flask, jsonify, request
from services.db_handler import MongoDBHandler
import threading

app = Flask(__name__)

# Set up MongoDB handler
db = MongoDBHandler()

@app.route('/')
def index():
    return "Middleware is running."

# Endpoint to GET current passenger counts and POST new passenger data
@app.route('/passenger_counts', methods=['GET', 'POST'])
def handle_passenger_counts():
    if request.method == 'GET':
        try:
            data = db.get_data("passenger_counts", {})
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            db.insert_data("passenger_counts", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to GET real-time environmental data and POST new environment data
@app.route('/environment_data', methods=['GET', 'POST'])
def handle_environment_data():
    if request.method == 'GET':
        try:
            data = db.get_data("environment_data", {})
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            db.insert_data("environment_data", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to GET real-time GPS data and POST new GPS data
@app.route('/gps_data', methods=['GET', 'POST'])
def handle_gps_data():
    if request.method == 'GET':
        try:
            data = db.get_data("gps_data", {})
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            db.insert_data("gps_data", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to get active alerts
@app.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        alerts = db.get_data("alerts", {})
        return jsonify(list(alerts)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the MQTT listener in a separate thread
if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt_listener, args=(db,))
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=5000)
