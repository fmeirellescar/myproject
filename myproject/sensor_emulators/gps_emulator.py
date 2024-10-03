# gps_emulator.py
import time
import random
import paho.mqtt.client as mqtt

# MQTT Broker configuration
BROKER = "mqtt_broker"
PORT = 1883
TOPIC = "vehicle/sensor_data/gps"

def simulate_gps_data():
    # Simulate random latitude and longitude for a specific area (e.g., Paris)
    latitude = round(random.uniform(48.85, 48.87), 5)
    longitude = round(random.uniform(2.29, 2.31), 5)
    return latitude, longitude

def publish_gps_data():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        latitude, longitude = simulate_gps_data()
        payload = f"Latitude: {latitude}, Longitude: {longitude}"
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(40)  # Send data every 10 seconds

if __name__ == "__main__":
    publish_gps_data()

