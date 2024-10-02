from datetime import datetime
import random
import paho.mqtt.client as mqtt

# Simulate validated tickets (ensure it's never higher than passenger count)
def simulate_validated_tickets(passenger_count):
    return random.randint(0.3*passenger_count, 0.9*passenger_count)

# Fare evasion detection logic
def check_fare_evasion(passenger_count, validated_tickets):
    # Ensure validated tickets are not higher than passenger count
    if validated_tickets > passenger_count:
        raise ValueError("Validated tickets cannot exceed passenger count")
    
    # Detect fare evasion
    if passenger_count > validated_tickets:
        evasion_count = passenger_count - validated_tickets
        print(f"Fare evasion detected: {evasion_count} passengers without valid tickets.")
        return True, evasion_count
    return False, 0

# MQTT message handler
def on_message(client, userdata, msg):
    db = userdata
    topic = msg.topic
    payload = msg.payload.decode()

    # Passenger data processing
    if "passenger_count" in topic:
        # Extract passenger count from payload
        passenger_count = int(payload.split(":")[1])

        # Simulate validated tickets for testing
        validated_tickets = simulate_validated_tickets(passenger_count)

        # Check for fare evasion
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
        db.insert_data("passenger_counts", data)

        # Store fare evasion alert if detected
        if fare_evasion_detected:
            alert = {
                "timestamp": datetime.utcnow(),
                "vehicle_id": "bus_123",  # Replace with actual vehicle ID
                "alert_type": "fare_evasion",
                "details": f"{evasion_count} passengers without valid tickets"
            }
            db.insert_data("alerts", alert)

    elif "environment" in topic:
        # Extract temperature and humidity from the payload
        temperature, humidity = payload.split(",")
        data = {
            "timestamp": datetime.utcnow(),
            "sensor_type": "environment",
            "vehicle_id": "bus_123",  # Replace with actual vehicle ID
            "temperature": float(temperature.split(":")[1].strip("C")),
            "humidity": float(humidity.split(":")[1].strip("%"))
        }
        # Store environmental data in MongoDB
        db.insert_data("environment_data", data)

    elif "gps" in topic:
        # Extract latitude and longitude from the payload
        latitude, longitude = payload.split(",")
        data = {
            "timestamp": datetime.utcnow(),
            "sensor_type": "gps",
            "vehicle_id": "bus_123",  # Replace with actual vehicle ID
            "latitude": float(latitude.split(":")[1]),
            "longitude": float(longitude.split(":")[1])
        }
        # Store GPS data in MongoDB
        db.insert_data("gps_data", data)


# Start MQTT listener
def start_mqtt_listener(db_handler):
    client = mqtt.Client(userdata=db_handler)
    client.on_message = on_message
    client.connect("mqtt_broker", 1883, 60)  # Connect to your MQTT broker
    client.subscribe("vehicle/sensor_data/#")  # Listen to all sensor topics
    client.loop_forever()
