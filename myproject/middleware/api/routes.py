from flask import Flask, jsonify, request
from services.db_handler import MongoDBHandler

app = Flask(__name__)
db = MongoDBHandler()

# Existing GET route to retrieve vehicle data
@app.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle_data(vehicle_id):
    query = {"vehicle_id": vehicle_id}
    data = db.get_data("passengers", query)
    return jsonify(list(data))

# Existing GET route to retrieve alerts
@app.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = db.get_data("alerts", {})
    return jsonify(list(alerts))

# New POST route to handle passenger count data
@app.route('/passenger_counts', methods=['POST'])
def passenger_counts():
    data = request.json
    # Insert the passenger count data into MongoDB
    db.insert_data("passenger_counts", data)
    return jsonify({"status": "success"}), 200

# New POST route to handle environmental data
@app.route('/environment_data', methods=['POST'])
def environment_data():
    data = request.json
    # Insert the environmental data into MongoDB
    db.insert_data("environment_data", data)
    return jsonify({"status": "success"}), 200

# New POST route to handle GPS data
@app.route('/gps_data', methods=['POST'])
def gps_data():
    data = request.json
    # Insert the GPS data into MongoDB
    db.insert_data("gps_data", data)
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
