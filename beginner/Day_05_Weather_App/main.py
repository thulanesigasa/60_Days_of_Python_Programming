import tkinter as tk
from tkinter import messagebox
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 5: Weather App")
        self.root.geometry("400x480")
        self.root.configure(bg="#121212")  # 60% Black
        self.root.resizable(False, False)

        # Header Label
        self.header_label = tk.Label(
            self.root, 
            text="WEATHER TRACKER", 
            font=("Helvetica", 16, "bold"), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue Accent
        )
        self.header_label.pack(pady=20)

        # Search Frame
        self.search_frame = tk.Frame(self.root, bg="#121212")
        self.search_frame.pack(fill="x", padx=30, pady=(0, 20))

        self.city_entry = tk.Entry(
            self.search_frame,
            font=("Helvetica", 12),
            bg="#1E293B",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            bd=0,
            relief="flat",
            justify="center"
        )
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.city_entry.insert(0, "London")
        self.city_entry.bind("<Return>", lambda event: self.get_weather())

        self.search_btn = tk.Button(
            self.search_frame,
            text="Search",
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF",
            activebackground="#2563EB",
            activeforeground="#FFFFFF",
            bd=0,
            padx=15,
            command=self.get_weather,
            cursor="hand2"
        )
        self.search_btn.pack(side="right", ipady=6)

        # Weather Display Frame
        self.display_frame = tk.Frame(self.root, bg="#1E293B", bd=0)
        self.display_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.city_label = tk.Label(
            self.display_frame,
            text="CITY NAME",
            font=("Helvetica", 16, "bold"),
            bg="#1E293B",
            fg="#FFFFFF"  # 10% White Accent
        )
        self.city_label.pack(pady=(20, 5))

        self.temp_label = tk.Label(
            self.display_frame,
            text="--°C",
            font=("Helvetica", 36, "bold"),
            bg="#1E293B",
            fg="#FFFFFF"
        )
        self.temp_label.pack(pady=10)

        self.desc_label = tk.Label(
            self.display_frame,
            text="Search for a city to display weather details",
            font=("Helvetica", 11, "italic"),
            bg="#1E293B",
            fg="#E2E8F0",
            wraplength=300
        )
        self.desc_label.pack(pady=5)

        self.details_label = tk.Label(
            self.display_frame,
            text="Humidity: --% | Wind: -- km/h",
            font=("Helvetica", 10),
            bg="#1E293B",
            fg="#2563EB"
        )
        self.details_label.pack(pady=15)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return

        # Attempt to use real API, but gracefully fall back to mock data if key is dummy or network fails
        api_key = "dummy_key_or_user_key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            if api_key == "dummy_key_or_user_key":
                raise ValueError("Dummy API Key")
            response = requests.get(url, timeout=4)
            data = response.json()
            if response.status_code == 200:
                self.update_weather_ui(
                    city=data["name"],
                    temp=round(data["main"]["temp"]),
                    desc=data["weather"][0]["description"].capitalize(),
                    humidity=data["main"]["humidity"],
                    wind=round(data["wind"]["speed"] * 3.6)
                )
            else:
                raise ValueError(data.get("message", "City not found"))
        except Exception:
            # Fallback mock weather database for demonstration purposes
            simulated_cities = {
                "london": {"temp": 15, "desc": "Light rain", "humidity": 80, "wind": 12},
                "new york": {"temp": 22, "desc": "Partly cloudy", "humidity": 55, "wind": 18},
                "tokyo": {"temp": 28, "desc": "Sunny", "humidity": 45, "wind": 8},
                "paris": {"temp": 18, "desc": "Overcast clouds", "humidity": 70, "wind": 14},
                "cape town": {"temp": 16, "desc": "Clear sky", "humidity": 60, "wind": 25},
            }
            city_lower = city.lower()
            if city_lower in simulated_cities:
                w = simulated_cities[city_lower]
                self.update_weather_ui(
                    city=city.title(),
                    temp=w["temp"],
                    desc=w["desc"] + " (Simulated)",
                    humidity=w["humidity"],
                    wind=w["wind"]
                )
            else:
                import random
                temps = [12, 18, 25, 30, 8, -2, 15]
                descs = ["Clear sky", "Cloudy", "Drizzle", "Showers", "Windy"]
                self.update_weather_ui(
                    city=city.title(),
                    temp=random.choice(temps),
                    desc=random.choice(descs) + " (Simulated)",
                    humidity=random.randint(30, 90),
                    wind=random.randint(5, 35)
                )

    def update_weather_ui(self, city, temp, desc, humidity, wind):
        self.city_label.config(text=city.upper())
        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=desc)
        self.details_label.config(text=f"Humidity: {humidity}% | Wind: {wind} km/h")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
