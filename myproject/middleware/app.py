from services.sensor_handler import start_mqtt_listener
from flask import Flask
from services.db_handler import MongoDBHandler
import threading

app = Flask(__name__)

# Set up MongoDB handler
db = MongoDBHandler()

@app.route('/')
def index():
    return "Middleware is running."

# Start the MQTT listener in a separate thread
if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt_listener, args=(db,))
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=5000)
