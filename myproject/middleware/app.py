from services.sensor_handler import start_mqtt_listener
from flask import Flask, jsonify, request
from services.db_handler import MongoDBHandler
import threading
from prometheus_client import start_http_server, Summary, generate_latest, CONTENT_TYPE_LATEST

# Set up the Prometheus summary metric
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

app = Flask(__name__)

# Set up MongoDB handler
db = MongoDBHandler()

@app.route('/')
@REQUEST_TIME.time()  # This will measure the time taken by this route
def index():
    return "Middleware is running."

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Endpoint to GET current passenger counts and POST new passenger data for a specific bus
@app.route('/passenger_counts/<vehicle_id>', methods=['GET', 'POST'])
@REQUEST_TIME.time()
def handle_passenger_counts(vehicle_id):
    if request.method == 'GET':
        try:
            query = {"vehicle_id": vehicle_id}
            data = db.get_data("passenger_counts", query)
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            data["vehicle_id"] = vehicle_id  # Associate data with the specific bus
            db.insert_data("passenger_counts", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to GET real-time environmental data and POST new environment data for a specific bus
@app.route('/environment_data/<vehicle_id>', methods=['GET', 'POST'])
@REQUEST_TIME.time()
def handle_environment_data(vehicle_id):
    if request.method == 'GET':
        try:
            query = {"vehicle_id": vehicle_id}
            data = db.get_data("environment_data", query)
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            data["vehicle_id"] = vehicle_id  # Associate data with the specific bus
            db.insert_data("environment_data", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to GET real-time GPS data and POST new GPS data for a specific bus
@app.route('/gps_data/<vehicle_id>', methods=['GET', 'POST'])
@REQUEST_TIME.time()
def handle_gps_data(vehicle_id):
    if request.method == 'GET':
        try:
            query = {"vehicle_id": vehicle_id}
            data = db.get_data("gps_data", query)
            return jsonify(list(data)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            data["vehicle_id"] = vehicle_id  # Associate data with the specific bus
            db.insert_data("gps_data", data)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to GET active alerts for a specific bus
@app.route('/alerts/<vehicle_id>', methods=['GET'])
@REQUEST_TIME.time()
def get_alerts(vehicle_id):
    try:
        query = {"vehicle_id": vehicle_id}
        alerts = db.get_data("alerts", query)
        return jsonify(list(alerts)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the MQTT listener in a separate thread
if __name__ == "__main__":
    # Start the Prometheus metrics server on port 8000
    start_http_server(8000)
    
    mqtt_thread = threading.Thread(target=start_mqtt_listener, args=(db,))
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=5000)
