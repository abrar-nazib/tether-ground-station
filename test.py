from tkinter import *
from tkintermapview import TkinterMapView
from PIL import Image, ImageDraw, ImageTk
import pandas as pd
import numpy as np
from colour import Color
# Function to create a gradient color based on signal strength
def get_gradient_color(signal_strength):
    # Define the range of signal strength values
    min_signal_strength = -100  # Worst signal strength
    max_signal_strength = -40   # Best signal strength

    # Normalize signal strength to the range [0, 1]
    normalized_signal = (signal_strength - min_signal_strength) / (max_signal_strength - min_signal_strength)

    # Create a gradient between red and green with 10 steps
    gradient_colors = list(Color("red").range_to(Color("#4CFF33"), 10))

    # Calculate the index in the gradient based on the normalized signal strength
    color_index = int(normalized_signal * (len(gradient_colors) - 1))

    # Get the color from the gradient
    selected_color = gradient_colors[color_index]

    # Convert the color to RGB and add transparency
    red, green, blue = selected_color.rgb
    return int(red * 255), int(green * 255), int(blue * 255), 128  # 50% transparency





# Function to create a marker image with gradient color
def create_marker_image(signal_strength):
    # Create a custom marker image using Pillow
    marker_image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))  # Create a transparent image

    # Create a drawing context
    marker_draw = ImageDraw.Draw(marker_image)

    # Calculate the circle's position and size
    circle_center = (16, 16)  # Center of the image
    circle_radius = 4  # 8px diameter circle, so radius is half of that

    # Get the gradient color based on signal strength
    circle_color = get_gradient_color(signal_strength)

    # Draw a circle with gradient color
    marker_draw.ellipse(
        [circle_center[0] - circle_radius, circle_center[1] - circle_radius,
         circle_center[0] + circle_radius, circle_center[1] + circle_radius],
        fill=circle_color
    )

    # Convert the Pillow image to a PhotoImage for use in tkinter
    marker_icon = ImageTk.PhotoImage(marker_image)
    return marker_icon

# Rest of your code remains the same
root = Tk()
root.title('Map with Custom Marker')

map_widget = TkinterMapView(root, width=800, height=600)
map_widget.pack()

def load_data():
    # Load your data
    # ...
    df = pd.read_csv('ML/drone_dataset.csv')
    df = df[df['altitude'] == 50]
    # take random 2000 samples
    df = df.sample(2000)
    return df

def put_marker(df, map_widget):
    # Place markers on the map with gradient colors
    for row in df.itertuples():
        marker_lat, marker_lng = row.lat, row.lng
        marker_icon = create_marker_image(row.signal_strength)
        map_widget.set_marker(marker_lat, marker_lng, icon=marker_icon)

df = load_data()
put_marker(df, map_widget)

root.mainloop()
