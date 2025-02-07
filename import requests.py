import folium
from geopy.geocoders import Nominatim
import requests
import matplotlib.pyplot as plt
import pandas as pd
import schedule
import time

# Geolocator
geolocator = Nominatim(user_agent="geo_tracker")

def fetch_trade_conflicts():
    url = "https://api.gdeltproject.org/api/v2/events/query"
    params = {
        'query': 'tariffs OR sanctions OR export ban',
        'format': 'json',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def update_conflicts():
    print("Fetching and updating conflict data...")
    trade_data = fetch_trade_conflicts()

    conflicts = []
    if trade_data:
        for event in trade_data.get("data", []):  # Adjust keys as per API response
            conflicts.append({
                "title": event.get("title", "No Title"),
                "location": event.get("location", "Unknown"),
                "type": event.get("type", "Uncategorized"),
            })

        # Geocode locations
        for conflict in conflicts:
            try:
                location = geolocator.geocode(conflict["location"])
                conflict["latitude"] = location.latitude if location else 0
                conflict["longitude"] = location.longitude if location else 0
            except Exception as e:
                print(f"Geocoding failed for {conflict['location']}: {e}")
                conflict["latitude"], conflict["longitude"] = 0, 0

        # Save map
        map = folium.Map(location=[20, 0], zoom_start=2)
        for conflict in conflicts:
            color = "blue" if conflict["type"] == "Trade" else "red" if conflict["type"] == "Sanction" else "green"
            folium.Marker(
                location=[conflict["latitude"], conflict["longitude"]],
                popup=f"{conflict['title']} ({conflict['type']})",
                icon=folium.Icon(color=color)
            ).add_to(map)
        map.save("geopolitical_map.html")
        print("Map updated.")

        # Plot chart
        df = pd.DataFrame(conflicts)
        type_counts = df["type"].value_counts()
        plt.bar(type_counts.index, type_counts.values)
        plt.title("Conflict Types Distribution")
        plt.xlabel("Conflict Type")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("No data to update.")

schedule.every(2).weeks.do(update_conflicts)

while True:
    schedule.run_pending()
    time.sleep(1)
