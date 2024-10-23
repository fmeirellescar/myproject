# passenger_emulator.py
import time
import random
import paho.mqtt.client as mqtt

# Broker information
BROKER = "mqtt_broker"
PORT = 1883
TOPIC = "vehicle/sensor_data/passenger_count"

# We set a standard bus_id but we will diferentiate it further
bus_id = "bus_1"  

def publish_sensor_data():
    client = mqtt.Client()
    client.connect(host=BROKER, port=PORT,keepalive= 60)

    while True:
        passenger_count = random.randint(10, 50)
        payload = f"BusID:{bus_id},PassengerCount:{passenger_count}"
        client.publish(topic=TOPIC, payload=payload)
        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()