# Use a lightweight Python image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install required Python packages
RUN pip install paho-mqtt

# Default command to run the passenger emulator (override in Compose)
CMD ["python", "passenger_emulator.py"]

