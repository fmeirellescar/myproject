# sensor_emulators/Dockerfile

FROM python:3.8-slim

WORKDIR /app

# Copy the sensor emulator scripts and bus logic
COPY . /app

# Install necessary dependencies
RUN pip install paho-mqtt

CMD ["python", "bus_manager.py"]
