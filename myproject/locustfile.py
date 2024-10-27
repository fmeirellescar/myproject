from locust import HttpUser, task, between
import random

class BusUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between tasks

    @task
    def send_gps_data(self):
        bus_id = f"bus_{random.randint(1, 1000)}"  # Randomly select a bus ID
        gps_data = {
            "latitude": round(random.uniform(48.85, 48.87), 5),
            "longitude": round(random.uniform(2.29, 2.31), 5)
        }
        self.client.post(f"/gps_data/{bus_id}", json=gps_data)

    @task
    def send_environment_data(self):
        bus_id = f"bus_{random.randint(1, 50)}"
        environment_data = {
            "temperature": round(random.uniform(10, 30), 2),
            "humidity": round(random.uniform(30, 80), 2)
        }
        self.client.post(f"/environment_data/{bus_id}", json=environment_data)

    @task
    def send_passenger_data(self):
        bus_id = f"bus_{random.randint(1, 50)}"
        passenger_data = {
            "passenger_count": random.randint(10, 50)
        }
        self.client.post(f"/passenger_counts/{bus_id}", json=passenger_data)
