# api/routes.py
from flask import Flask, jsonify
from services.db_handler import MongoDBHandler

app = Flask(__name__)
db = MongoDBHandler()

@app.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle_data(vehicle_id):
    query = {"vehicle_id": vehicle_id}
    data = db.get_data("passengers", query)
    return jsonify(list(data))

@app.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = db.get_data("alerts", {})
    return jsonify(list(alerts))

if __name__ == "__main__":
    app.run(debug=True)

