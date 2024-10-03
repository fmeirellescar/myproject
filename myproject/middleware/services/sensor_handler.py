import logging
from datetime import datetime
import random
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Simulate validated tickets (In reality this data would be retrieved from the validation database from SNCF)
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

# MQTT message handler
def on_message(client, userdata, msg):
    db = userdata
    topic = msg.topic
    payload = msg.payload.decode()

    logging.info(f"Received message on topic {topic}: {payload}")

    try:
        if "passenger_count" in topic:
            # Process passenger data
            passenger_count = int(payload.split(":")[1])
            validated_tickets = simulate_validated_tickets(passenger_count)
            fare_evasion_detected, evasion_count = check_fare_evasion(passenger_count, validated_tickets)

            # Prepare data to store in MongoDB
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "passenger_count",
                "vehicle_id": "bus_123",  # Replace with actual vehicle ID
                "passenger_count": passenger_count,
                "validated_tickets": validated_tickets,
                "fare_evasion_detected": fare_evasion_detected,
                "evasion_count": evasion_count
            }
            logging.info(f"Inserting passenger count data into MongoDB: {data}")
            db.insert_data("passenger_counts", data)

            if fare_evasion_detected:
                alert = {
                    "timestamp": datetime.utcnow(),
                    "vehicle_id": "bus_123",
                    "alert_type": "fare_evasion",
                    "details": f"{evasion_count} passengers without valid tickets"
                }
                logging.info(f"Inserting fare evasion alert into MongoDB: {alert}")
                db.insert_data("alerts", alert)

        elif "environment" in topic:
            temperature, humidity = payload.split(",")
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "environment",
                "vehicle_id": "bus_123",
                "temperature": float(temperature.split(":")[1].strip("C")),
                "humidity": float(humidity.split(":")[1].strip("%"))
            }
            logging.info(f"Inserting environmental data into MongoDB: {data}")
            db.insert_data("environment_data", data)

        elif "gps" in topic:
            latitude, longitude = payload.split(",")
            data = {
                "timestamp": datetime.utcnow(),
                "sensor_type": "gps",
                "vehicle_id": "bus_123",
                "latitude": float(latitude.split(":")[1]),
                "longitude": float(longitude.split(":")[1])
            }
            logging.info(f"Inserting GPS data into MongoDB: {data}")
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
