#bus.py
import random
import time
import paho.mqtt.client as mqtt
from threading import Thread

class Bus:
    bus_counter = 0

    def __init__(self):
        # Increment the bus ID
        Bus.bus_counter += 1
        self.bus_id = f"bus_{Bus.bus_counter}"

        # MQTT client setup
        self.client = mqtt.Client()
        self.client.connect("mqtt_broker", 1883, 60)
        
        # Initial sensor values (simulated)
        self.gps = {"latitude": round(random.uniform(48.85, 48.87), 5), "longitude": round(random.uniform(2.29, 2.31), 5)}
        self.environment = {"temperature": random.uniform(10, 30), "humidity": random.uniform(30, 80)}
        self.passenger_count = random.randint(10, 50)

    def generate_gps_data(self):
        # Simulate slight movement in GPS coordinates
        self.gps["latitude"] += random.uniform(-0.001, 0.001)
        self.gps["longitude"] += random.uniform(-0.001, 0.001)
        return f"Latitude: {self.gps['latitude']}, Longitude: {self.gps['longitude']}"

    def generate_environment_data(self):
        # Simulate environmental changes
        self.environment["temperature"] += random.uniform(-0.1, 0.1)
        self.environment["humidity"] += random.uniform(-0.5, 0.5)
        return f"Temperature: {self.environment['temperature']}C, Humidity: {self.environment['humidity']}%"

    def generate_passenger_data(self):
        # Simulate passenger changes
        self.passenger_count = min(50, max(0, self.passenger_count + random.randint(-7, 7)))
        return f"PassengerCount: {self.passenger_count}"

    def send_data(self):
        # Simulate sending sensor data to MQTT broker
        while True:
            gps_data = self.generate_gps_data()
            environment_data = self.generate_environment_data()
            passenger_data = self.generate_passenger_data()

            # Publish data to respective topics
            self.client.publish(f"vehicle/sensor_data/gps/{self.bus_id}", gps_data)
            self.client.publish(f"vehicle/sensor_data/environment/{self.bus_id}", environment_data)
            self.client.publish(f"vehicle/sensor_data/passenger_count/{self.bus_id}", passenger_data)

            # Simulate delay between messages
            time.sleep(40)

    def start(self):
        # Start the sensor data transmission in a separate thread
        thread = Thread(target=self.send_data)
        thread.start()
