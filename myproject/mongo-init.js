// Initialize MongoDB indexes when the container starts

db = db.getSiblingDB('transport_db');

// Insert a dummy document to create the collection if it doesn't exist
db.passenger_counts.insertOne({ vehicle_id: 'dummy', timestamp: new Date() });
db.environment_data.insertOne({ vehicle_id: 'dummy', timestamp: new Date() });
db.gps_data.insertOne({ vehicle_id: 'dummy', timestamp: new Date() });
db.alerts.insertOne({ vehicle_id: 'dummy', timestamp: new Date() });

// Index for passenger_counts collection
db.passenger_counts.createIndex({ vehicle_id: 1 });
db.passenger_counts.createIndex({ timestamp: 1 });

// Index for environment_data collection
db.environment_data.createIndex({ vehicle_id: 1 });
db.environment_data.createIndex({ timestamp: 1 });

// Index for gps_data collection
db.gps_data.createIndex({ vehicle_id: 1 });
db.gps_data.createIndex({ timestamp: 1 });

// Index for alerts collection
db.alerts.createIndex({ vehicle_id: 1 });
db.alerts.createIndex({ timestamp: 1 });

// Remove the dummy documents after indexes are created
db.passenger_counts.deleteOne({ vehicle_id: 'dummy' });
db.environment_data.deleteOne({ vehicle_id: 'dummy' });
db.gps_data.deleteOne({ vehicle_id: 'dummy' });
db.alerts.deleteOne({ vehicle_id: 'dummy' });