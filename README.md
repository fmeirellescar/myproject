# Middleware for Smart Bus Monitoring System

This project is a middleware solution designed for a smart bus monitoring system. The middleware interacts with multiple sensor emulators, processes real-time data, and stores it in MongoDB. It also integrates monitoring tools like Prometheus and Grafana for analytics and alerting. Alerts for high unvalidated passenger counts are sent via Discord webhook notifications to a dedicated server. This guide provides step-by-step instructions to set up and run the system using Docker.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Architecture](#system-architecture)
3. [Setup Instructions](#setup-instructions)
   - [1. Clone the Repository](#1-clone-the-repository)
   - [2. Configure Docker](#2-configure-docker)
   - [3. Start the Containers](#3-start-the-containers)
   - [4. Access the System](#4-access-the-system)
4. [Key Components](#key-components)
5. [Testing and Validation](#testing-and-validation)
6. [Monitoring and Alerts](#monitoring-and-alerts)
7. [Troubleshooting](#troubleshooting)
8. [Team Contributions](#team-contributions)

---

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8 or above (for local development and running standalone scripts)

---

## System Architecture

The system consists of the following components:

- **Sensor Emulators**: Simulate GPS, environmental, and passenger count data from multiple buses.
- **Middleware**: Processes incoming data, stores it in MongoDB, and exposes APIs for interaction. Also sends high unvalidated passenger alerts to Discord.
- **MongoDB**: Stores all sensor data, alerts, and logs.
- **Prometheus**: Monitors real-time metrics, which are visualized in Grafana dashboards.
- **Grafana**: Visualizes metrics for system monitoring and analysis.
- **Locust**: Conducts performance testing for the system.

### Diagram

A system architecture diagram visually representing the interaction between components is essential. It should include:

- Sensor emulators (GPS, environmental, passenger count)
- MQTT broker for communication
- Middleware (data processing and Prometheus metrics exposure)
- MongoDB for storage
- Prometheus and Grafana for monitoring
- Discord webhook for alerts

---

## Setup Instructions

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-repo/smart-bus-monitoring.git
cd smart-bus-monitoring
```

### 2. Configure Docker

Ensure all required Docker configuration files are present:

- `docker-compose.yml`
- `Dockerfile` for middleware and emulators
- `prometheus.yml` for Prometheus configuration
- `mosquitto.conf` for MQTT broker configuration

Modify configurations as needed:

- Update environment variables in `config.py` for database and broker settings.
- Set up the Prometheus scrape targets in `prometheus.yml`.

### 3. Start the Containers

Build and start the system using Docker Compose:

```bash
# Build the Docker containers
docker-compose build

# Start the containers
docker-compose up -d
```

Verify that the containers are running:

```bash
docker ps
```

### 4. Access the System

#### Middleware API

- **Base URL**: `http://localhost:5000`
- **Endpoints**:
  - `GET /vehicles/<vehicle_id>`: Retrieve vehicle data.
  - `POST /passenger_counts`: Insert passenger count data.
  - `POST /environment_data`: Insert environmental data.
  - `POST /gps_data`: Insert GPS data.

#### Monitoring Tools

- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`
  - Default username: `admin`
  - Default password: `admin`

#### Locust (Performance Testing)

- **Locust Web Interface**: `http://localhost:8089`
  - Use this interface to configure and run load tests.

---

## Key Components

### Middleware

The middleware processes real-time data, stores it in MongoDB, updates Prometheus metrics, and sends alerts to Discord via webhook.

**Code Snippet (Alert Logic Example):**

```python
if unvalidated_passengers > 10:
    alert_message = {
        "content": f"High unvalidated passenger count ({unvalidated_passengers}) on {vehicle_id}."
    }
    requests.post(DISCORD_WEBHOOK_URL, json=alert_message)
```

### Sensor Emulators

Simulate GPS, environmental, and passenger count data for multiple buses.

**Code Snippet (Simulating Bus Data):**

```python
def generate_gps_data(self):
    self.gps["latitude"] += random.uniform(-0.001, 0.001)
    self.gps["longitude"] += random.uniform(-0.001, 0.001)
    return f"Latitude: {self.gps['latitude']}, Longitude: {self.gps['longitude']}"
```

### MongoDB

Stores data in the following collections:

- `passenger_counts`: Passenger count data.
- `environment_data`: Environmental sensor data.
- `gps_data`: GPS location data.
- `alerts`: High unvalidated passenger alerts.

### Monitoring Tools

- **Prometheus**: Scrapes metrics exposed by the middleware.
- **Grafana**: Visualizes data and creates dashboards.

---

## Testing and Validation

### Performance Testing with Locust

1. Start the Locust container:

```bash
docker-compose up locust -d
```

2. Open the Locust Web Interface at `http://localhost:8089`.
3. Configure the number of users and spawn rate, then start the test.

### Middleware Logs

To view real-time logs:

```bash
docker logs -f <middleware-container-id>
```

---

## Monitoring and Alerts

### Prometheus

- Verify metrics using queries like `unvalidated_passengers_count` and `occupancy_percentage`.

### Grafana

1. Import a pre-configured dashboard or create custom visualizations.
2. Visualize metrics like passenger count, GPS locations, and environmental conditions.

### Discord Webhook Alerts

High unvalidated passenger counts (>10) trigger alerts sent to a Discord channel:

- Example alert: **"High unvalidated passenger count (12) on bus\_5."**

---

## Troubleshooting

- **Prometheus Not Scraping Data**: Verify `prometheus.yml` configuration and ensure the middleware is exposing metrics on `http://localhost:8000/metrics`.
- **Grafana Dashboard Empty**: Check Prometheus scrape targets and ensure data is being collected.
- **Discord Alerts Not Working**: Ensure the webhook URL is correctly set in the middleware.
- **Containers Not Starting**: Verify Docker Compose logs for errors and resolve any missing dependencies.

---

## Team Contributions

- **Middleware Development**: Real-time data processing and alerting logic.
- **Sensor Emulators**: Simulated multiple buses with GPS, environmental, and passenger count data.
- **Monitoring Tools**: Integrated Prometheus and Grafana for analytics.
- **Alerts System**: Configured Discord webhooks for high unvalidated passenger count alerts.

---

## Team Credits

This project was developed by Felipe Meirelles Carvalho Orlando and Abbas Alawieh in October 2024.

---

This concludes the setup and usage guide for the smart bus monitoring system. For further assistance, refer to the documentation or contact the development team.


