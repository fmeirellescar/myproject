import logging
from datetime import datetime
import random
import paho.mqtt.client as mqtt
import requests
from prometheus_client import Gauge
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prometheus Gauges for monitoring
unvalidated_passengers_gauge = Gauge('unvalidated_passengers_count', 'Number of unvalidated passengers per vehicle', ['vehicle_id'])
occupancy_gauge = Gauge('occupancy_percentage', 'Percentage of occupancy in the vehicle', ['vehicle_id'])
temperature_gauge = Gauge('vehicle_temperature', 'Temperature inside the vehicle', ['vehicle_id'])
humidity_gauge = Gauge('vehicle_humidity', 'Humidity inside the vehicle', ['vehicle_id'])

# Discord webhook URL for notifications
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1299387053884309605/D4jjgSf2NrAJG3qhikhjX9J96XeJNEBHOFuKxymQ5C0yAUCq1cxGDFU22w9Q4vo48JIF"

# MongoDB client for accessing GPS data
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["transport_db"]


# Simulate validated tickets (ensure it's never higher than passenger count)
def simulate_validated_tickets(passenger_count):
    lower_bound = int(0.3 * passenger_count)
    upper_bound = int(0.9 * passenger_count)
    return random.randint(lower_bound, upper_bound)

# Fare evasion detection logic
def check_fare_evasion(passenger_count, validated_tickets):
    if validated_tickets > passenger_count:
        raise ValueError("Validated tickets cannot exceed passenger count")
    
    if passenger_count > validated_tickets:
        evasion_count = passenger_count - validated_tickets
        logging.info(f"Fare evasion detected: {evasion_count} passengers without valid tickets.")
        return True, evasion_count
    return False, 0
# Retrieve latest GPS position from MongoDB
def get_latest_gps_position(vehicle_id):
    try:
        gps_data = db["gps_data"].find_one(
            {"vehicle_id": vehicle_id},
            sort=[("timestamp", -1)]
        )
        if gps_data:
            return gps_data["latitude"], gps_data["longitude"]
        else:
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving GPS data for {vehicle_id}: {e}")
        return None, None

# Send Discord alert if evasion count exceeds threshold, including GPS position
def send_discord_alert(vehicle_id, evasion_count):
    if evasion_count > 20:
        latitude, longitude = get_latest_gps_position(vehicle_id)
        location_info = f"Latitude: {latitude}, Longitude: {longitude}" if latitude and longitude else "Location data unavailable"

        message = {
            "content": f"🚨 Alert: High fare evasion detected! 🚨\n"
                       f"Vehicle ID: {vehicle_id}\n"
                       f"Unvalidated Tickets: {evasion_count}\n"
                       f"GPS Position: {location_info}\n"
                       f"Timestamp: {datetime.utcnow().isoformat()}",
        }
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=message)
            response.raise_for_status()
            logging.info(f"Discord alert sent for vehicle {vehicle_id} with {evasion_count} unvalidated tickets.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Discord alert: {e}")

# Update Prometheus metrics
def update_metrics(vehicle_id, unvalidated_passengers, occupancy_percentage, temperature, humidity):
    if unvalidated_passengers is not None:
        unvalidated_passengers_gauge.labels(vehicle_id).set(unvalidated_passengers)
    if occupancy_percentage is not None:
        occupancy_gauge.labels(vehicle_id).set(occupancy_percentage)
    if temperature is not None:
        temperature_gauge.labels(vehicle_id).set(temperature)
    if humidity is not None:
        humidity_gauge.labels(vehicle_id).set(humidity)

# MQTT message handler
def on_message(client, userdata, msg):
    db = userdata
    topic = msg.topic
    payload = msg.payload.decode()

    logging.info(f"Received message on topic {topic}: {payload}")

    try:
        # Extract sensor type and vehicle_id correctly from topic
        topic_parts = topic.split("/")
        sensor_type = topic_parts[2]
        vehicle_id = topic_parts[3]  # Correct vehicle ID extraction

        if "passenger_count" in sensor_type:
            # Process passenger data
            passenger_count = int(payload.split(":")[1])
            validated_tickets = simulate_validated_tickets(passenger_count)
            fare_evasion_detected, evasion_count = check_fare_evasion(passenger_count, validated_tickets)

            # Prepare data to store in MongoDB
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "passenger_count",
                "vehicle_id": vehicle_id,
                "passenger_count": passenger_count,
                "validated_tickets": validated_tickets,
                "fare_evasion_detected": fare_evasion_detected,
                "evasion_count": evasion_count
            }

            # Insert passenger data in MongoDB
            db.insert_data("passenger_counts", data)

            # Calculate occupancy and update metrics
            occupancy_percentage = (passenger_count / 50) * 100  # Assume bus capacity of 50
            update_metrics(vehicle_id, evasion_count, occupancy_percentage, None, None)

            # Send Discord alert if fare evasion threshold is met
            send_discord_alert(vehicle_id, evasion_count)

        elif "environment" in sensor_type:
            # Process environmental data
            temperature, humidity = payload.split(",")
            temp_value = float(temperature.split(":")[1].strip("C"))
            hum_value = float(humidity.split(":")[1].strip("%"))
            
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "environment",
                "vehicle_id": vehicle_id,
                "temperature": temp_value,
                "humidity": hum_value
            }

            # Insert environmental data in MongoDB
            db.insert_data("environment_data", data)

            # Update metrics for temperature and humidity
            update_metrics(vehicle_id, None, None, temp_value, hum_value)

        elif "gps" in sensor_type:
            # Process GPS data
            latitude, longitude = payload.split(",")
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "gps",
                "vehicle_id": vehicle_id,
                "latitude": float(latitude.split(":")[1]),
                "longitude": float(longitude.split(":")[1])
            }

            # Insert GPS data in MongoDB
            db.insert_data("gps_data", data)

    except Exception as e:
        logging.error(f"Error processing message on topic {topic}: {str(e)}", exc_info=True)

# Start MQTT listener
def start_mqtt_listener(db_handler):
    client = mqtt.Client(userdata=db_handler)
    client.on_message = on_message
    try:
        client.connect("mqtt_broker", 1883, 60)
        logging.info("Connected to MQTT broker")
        client.subscribe("vehicle/sensor_data/#")
        logging.info("Subscribed to vehicle/sensor_data/# topic")
        client.loop_forever()
    except Exception as e:
        logging.error(f"Failed to connect or subscribe to MQTT broker: {str(e)}", exc_info=True)
