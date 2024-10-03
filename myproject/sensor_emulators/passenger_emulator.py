# passenger_emulator.py
import time
import random
import paho.mqtt.client as mqtt

# Update BROKER to the Docker service name "mqtt_broker"
BROKER = "mqtt_broker"
PORT = 1883
TOPIC = "vehicle/sensor_data/passenger_count"

def simulate_passenger_count():
    return random.randint(10, 50)

def publish_sensor_data():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        passenger_count = simulate_passenger_count()
        client.publish(TOPIC, f"PassengerCount: {passenger_count}")
        print(f"Published PassengerCount: {passenger_count}")
        time.sleep(40)

if __name__ == "__main__":
    publish_sensor_data()
