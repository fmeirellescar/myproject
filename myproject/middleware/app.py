# app.py
from api.routes import app
from services.sensor_handler import start_mqtt_listener
import threading

if __name__ == "__main__":
    # Start the MQTT listener in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_listener)
    mqtt_thread.start()

    # Start the Flask API for UI interaction
    app.run(host="0.0.0.0", port=5000)

