# environment_emulator.py
import time
import random
import paho.mqtt.client as mqtt

# MQTT Broker configuration
BROKER = "mqtt_broker"
PORT = 1883
TOPIC = "vehicle/sensor_data/environment"

def simulate_environment_data():
    # Simulate random temperature and humidity readings
    temperature = round(random.uniform(18.0, 25.0), 2)  # in °C
    humidity = round(random.uniform(30.0, 60.0), 2)  # in %
    return temperature, humidity

def publish_environment_data():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        temperature, humidity = simulate_environment_data()
        payload = f"Temperature: {temperature}C, Humidity: {humidity}%"
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(40)  # Send data every 10 seconds

if __name__ == "__main__":
    publish_environment_data()
