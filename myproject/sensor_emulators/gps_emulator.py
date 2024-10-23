# gps_emulator.py
import time
import random
import paho.mqtt.client as mqtt

# Broker information
BROKER = "mqtt_broker"
PORT = 1883
TOPIC = "vehicle/sensor_data/passenger_count"

# We set a standard bus_id but we will diferentiate it further
bus_id = "bus_1" 

def publish_gps_data():
    client = mqtt.Client()
    client.connect(host=BROKER, port=PORT, keepalive=60)

    while True:
        latitude = round(random.uniform(48.85, 48.90), 5)
        longitude = round(random.uniform(2.29, 2.35), 5)
        payload = f"BusID:{bus_id},Latitude:{latitude},Longitude:{longitude}"
        client.publish(topic=TOPIC, payload=payload)
        time.sleep(5)

if __name__ == "__main__":
    publish_gps_data()
