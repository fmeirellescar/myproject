# services/sensor_handler.py
import paho.mqtt.client as mqtt
from services.db_handler import MongoDBHandler

db = MongoDBHandler()

# MQTT callback to handle incoming messages
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message: {payload} from topic: {topic}")

    # Process message and store in MongoDB
    data = {"sensor_data": payload, "topic": topic}
    db.insert_data("sensors", data)

# MQTT setup
def start_mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)  # Use your actual broker
    client.subscribe("vehicle/sensor_data")
    client.loop_forever()

