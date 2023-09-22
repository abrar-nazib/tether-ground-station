import csv
import math
import random

# Constants
tower_lat = 23.7489144
tower_lng = 90.3703079
altitude = 50  # meters
min_distance = 1  # meters
max_distance = 100  # meters
min_readings = 10
max_readings = 100

# Create a CSV file to write the data
with open('drone_signal_strength_dataset.csv', 'w', newline='') as csvfile:
    fieldnames = ['lat', 'lng', 'altitude', 'tower_distance', 'signal_strength']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Generate data for each distance from min_distance to max_distance
    for distance in range(min_distance, max_distance + 1):
        # Calculate the circumference of the circle
        circumference = 2 * math.pi * distance

        # Calculate the number of points (readings) in the circle
        num_points = random.randint(min_readings, max_readings)

        # Generate data for each point
        for _ in range(num_points):
            # Calculate the angle for this point
            angle = random.uniform(0, 2 * math.pi)

            # Calculate the latitude and longitude for the point
            lat = tower_lat + (distance / 111.32) * math.cos(angle)
            lng = tower_lng + (distance / (111.32 * math.cos(math.radians(tower_lat)))) * math.sin(angle)

            # Calculate signal strength (exponential decrease with Gaussian noise)
            tower_distance = distance
            signal_strength = math.exp(-distance / 20) + random.gauss(0, 0.1)

            # Write data to the CSV file
            writer.writerow({
                'lat': lat,
                'lng': lng,
                'altitude': altitude,
                'tower_distance': tower_distance,
                'signal_strength': signal_strength
            })

print("Dataset generation complete.")
