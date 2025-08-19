import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from itertools import combinations
from shapely.geometry import LineString

# 1. Load city data
cities = pd.read_csv("german_cities_with_gdp.csv")
cities["GDP_Billion"] = pd.to_numeric(cities["GDP_Billion"], errors="coerce")
cities = cities.dropna(subset=["Population", "GDP_Billion", "Latitude", "Longitude"]).copy()

# 2. Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    φ1, φ2 = np.radians(lat1), np.radians(lat2)
    Δφ = φ2 - φ1
    Δλ = np.radians(lon2 - lon1)
    a = np.sin(Δφ / 2)**2 + np.cos(φ1) * np.cos(φ2) * np.sin(Δλ / 2)**2
    return R * (2 * np.arcsin(np.sqrt(a)))

# 3. Compute gravity flows with distance squared and K = 64380.06
K = 64380.06
records = []
for c1, c2 in combinations(cities.to_dict('records'), 2):
    mass1 = c1["Population"] * c1["GDP_Billion"]
    mass2 = c2["Population"] * c2["GDP_Billion"]
    d = haversine(c1["Latitude"], c1["Longitude"], c2["Latitude"], c2["Longitude"])
    if d <= 0:
        flow = 0
    else:
        flow = K * (mass1 * mass2) / (d**2)

    records.append({
        "City1": c1["CityName"],
        "City2": c2["CityName"],
        "Flow": flow,
        "lat1": c1["Latitude"],
        "lon1": c1["Longitude"],
        "lat2": c2["Latitude"],
        "lon2": c2["Longitude"]
    })

flows_df = pd.DataFrame(records)
flows_df.to_csv("germany_gravity_flows_distsq.csv", index=False)
print("Saved flows to germany_gravity_flows_distsq.csv")
