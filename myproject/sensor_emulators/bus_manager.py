# sensor_emulators/bus_manager.py

from bus import Bus

def create_buses(num_buses):
    buses = []
    for _ in range(num_buses):
        bus = Bus()
        bus.start()
        buses.append(bus)
    return buses

if __name__ == "__main__":
    # Create 50 bus instances
    create_buses(50)
