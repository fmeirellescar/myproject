# Use a lightweight Python image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install required Python packages
RUN pip install pymongo paho-mqtt flask requests prometheus_client

# Expose the API port
EXPOSE 5000

# Default command to run the middleware
CMD ["python", "app.py"]

