import random
import csv
from math import cos, sin, pi, exp

# Constants
tower_latitude = 23.7489144
tower_longitude = 90.3703079
altitude = 50  # meters
min_radius = 1  # meter
max_radius = 100  # meters
min_readings_per_circle = 10
max_readings_per_circle = 100

# Function to generate signal strength with exponential decay and noise
def generate_signal_strength(radius):
    # Exponential signal strength decay with added noise
    base_signal_strength = -50 - 20 * (1 - exp(-radius / 50))
    signal_strength = base_signal_strength + random.gauss(0, 5)
    return max(signal_strength, -120)  # Ensure signal strength is within the specified range

# Generate and write data to CSV
with open('drone_dataset.csv', 'w', newline='') as csvfile:
    fieldnames = ['lat', 'lng', 'altitude', 'tower_distance', 'signal_strength']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for radius in range(min_radius, max_radius + 1):
        num_readings = random.randint(min_readings_per_circle, max_readings_per_circle)
        for _ in range(num_readings):
            # Calculate latitude and longitude for points around the tower
            theta = random.uniform(0, 2 * pi)
            lat = tower_latitude + (radius / 111000) * sin(theta)
            lng = tower_longitude + (radius / (111000 * cos(tower_latitude))) * cos(theta)
            
            # Calculate signal strength
            signal_strength = generate_signal_strength(radius)

            # Write data to CSV
            writer.writerow({'lat': lat, 'lng': lng, 'altitude': altitude, 'tower_distance': radius, 'signal_strength': signal_strength})

print("Dataset generated successfully.")
