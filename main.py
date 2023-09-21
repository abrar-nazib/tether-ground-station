ENV = "prod"  # Set to "dev" or "prod" to change the environment


import customtkinter
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import os
import requests
import json
import time 
import threading

# Absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_URL = "http://localhost:8080" if ENV == "dev" else "https://tether-s2ng.onrender.com"

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Tether"
    WIDTH = 1400
    HEIGHT = 800


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window properties
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        
        

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)  # Left panel will not resize in the x direction when the screen is resized
        self.grid_columnconfigure(1, weight=1) # Right panel will resize in the x direction when the screen is resized
        self.grid_rowconfigure(0, weight=1)  # Both panels will resize in the y direction when the screen is resized

        # Left panel attach
        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Right panel attach
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        # Run Plan button
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Run Plan",
                                                command=self.run_plan)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        # Clear Plan button
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Plan",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        
        # View Plot button
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="View Heatmap",
                                                command=self.view_heatmap)
        self.button_3.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        # Section for selecting map type
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=[ "Google normal", "OpenStreetMap", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        # Section for selecting theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        
        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)  # Run search_event() function on enter press

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Add an option to add marker in the right click menu
        self.map_widget.add_right_click_menu_command(label="Add marker", command=self.add_marker, pass_coords=True)

        # Set default values
        self.map_widget.set_address("Dhaka")
        self.map_option_menu.set("Google normal")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.appearance_mode_optionemenu.set("Dark")
        self.droneMarker = None        

        # Load marker icons
        self.marker_icon = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "images", "marker.png")).resize((40, 40)))
        self.drone_icon = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "images", "drone.png")).resize((40, 40)))


    def get_drone_position(self):
        while True:
            time.sleep(5)
            # Make a request to the server to get the drone location
            response = requests.get(f"{SERVER_URL}/drone-control/position")
            location = json.loads(response.content)
            if(self.droneMarker != None):
                self.droneMarker.delete()
            self.droneMarker = self.map_widget.set_marker(location["lat"], location["lng"], "Drone", icon=self.drone_icon)
            print(location)
            
    def add_marker(self, coords=None):
        marker = self.map_widget.set_marker(coords[0], coords[1], f"Point {len(self.marker_list) + 1}", icon=self.marker_icon)
        self.marker_list.append(marker)

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def run_plan(self):
        # Accumulate the lattitude and longitude from the marker list and send it to the server
        positions = []
        for marker in self.marker_list:
            d = {"lat": marker.position[0], "lng": marker.position[1]}
            positions.append(d)
        # make a request to the server
        response = requests.post(f"{SERVER_URL}/drone-control/plan", json=positions)
        print(response.content)
        
    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()
        self.marker_list = []

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    
    def view_heatmap(self):
        # Make a request to the server to get the signals
        response = requests.get(f"{SERVER_URL}/signal-data")
        signals = json.loads(response.content)
        print(signals)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    t = threading.Thread(target=app.get_drone_position)
    t.start()
    app.start()