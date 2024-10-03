from locust import HttpUser, TaskSet, task, between

class VehicleBehavior(TaskSet):
    @task(1)
    def send_passenger_data(self):
        self.client.post("/passenger_counts", json={
            "vehicle_id": "bus_123",
            "passenger_count": 35
        })

    @task(1)
    def send_environment_data(self):
        self.client.post("/environment_data", json={
            "vehicle_id": "bus_123",
            "temperature": 22.5,
            "humidity": 50.3
        })

    @task(1)
    def send_gps_data(self):
        self.client.post("/gps_data", json={
            "vehicle_id": "bus_123",
            "latitude": 48.8566,
            "longitude": 2.3522
        })

class VehicleUser(HttpUser):
    tasks = [VehicleBehavior]
    wait_time = between(1, 3)  # Simulates a 1 to 3 second delay between requests
