import random
import csv
from math import cos, sin, pi, exp

# Constants
tower_latitude = 23.7489144
tower_longitude = 90.3703079
altitudes = [60, 50, 40]  # meters
min_radius = 1  # meter
max_radius = 50  # meters  # Reduced max radius for faster generation
min_readings_per_circle = 10
max_readings_per_circle = 100

# Function to generate signal strength with altitude-dependent exponential decay and noise
def generate_signal_strength(radius, altitude):
    # Exponential signal strength decay with added noise, altitude-dependent
    if altitude == 60:
        base_signal_strength = -50 - 15 * (1 - exp(-radius / 20))
    elif altitude == 50:
        base_signal_strength = -50 - 20 * (1 - exp(-radius / 20))
    elif altitude == 40:
        base_signal_strength = -50 - 25 * (1 - exp(-radius / 20))

    signal_strength = base_signal_strength + random.gauss(0, 5)
    return max(signal_strength, -120)  # Ensure signal strength is within the specified range

# Generate and write data to CSV
with open('drone_dataset.csv', 'w', newline='') as csvfile:
    fieldnames = ['lat', 'lng', 'altitude', 'tower_distance', 'signal_strength']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for altitude in altitudes:
        for radius in range(min_radius, max_radius + 1):
            num_readings = random.randint(min_readings_per_circle, max_readings_per_circle)
            for _ in range(num_readings):
                # Calculate latitude and longitude for points around the tower
                theta = random.uniform(0, 2 * pi)
                lat = tower_latitude + (radius / 111000) * sin(theta)
                lng = tower_longitude + (radius / (111000 * cos(tower_latitude))) * cos(theta)
                
                # Calculate signal strength
                signal_strength = generate_signal_strength(radius, altitude)

                # Write data to CSV
                writer.writerow({'lat': lat, 'lng': lng, 'altitude': altitude, 'tower_distance': radius, 'signal_strength': signal_strength})

print("Dataset generated successfully.")
