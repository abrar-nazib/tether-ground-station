from tkinter import *
from tkintermapview import TkinterMapView
from PIL import Image, ImageDraw, ImageTk

root = Tk()
root.title('Map with Custom Marker')

map_widget = TkinterMapView(root, width=800, height=600)
map_widget.pack()

# Create a custom marker image using Pillow
marker_image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))  # Create a transparent image

# Create a drawing context
marker_draw = ImageDraw.Draw(marker_image)

# Define the rectangle color with semi-transparency (e.g., 50% transparency)
rectangle_color = (255, 0, 0, 128)  # (R, G, B, A) - 128 indicates 50% transparency

# Draw a red rectangle with semi-transparency
marker_draw.rectangle([0, 0, 31, 31], fill=rectangle_color, outline="black", width=2)  # Add a black border

# Convert the Pillow image to a PhotoImage for use in tkinter
marker_icon = ImageTk.PhotoImage(marker_image)

# Latitude and longitude of the marker's position
marker_lat, marker_lng = 48.860381, 2.338594

# Add a marker to the map with the custom semi-transparent icon
map_widget.set_marker(marker_lat, marker_lng, icon=marker_icon)

root.mainloop()
