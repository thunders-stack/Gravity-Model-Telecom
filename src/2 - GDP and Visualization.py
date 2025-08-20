# The function script
import pandas as pd
import numpy as np
from itertools import combinations
from shapely.geometry import LineString
import geopandas as gpd
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    φ1, φ2 = np.radians(lat1), np.radians(lat2)
    Δφ = φ2 - φ1
    Δλ = np.radians(lon2 - lon1)
    a = np.sin(Δφ / 2)**2 + np.cos(φ1) * np.cos(φ2) * np.sin(Δλ / 2)**2
    return R * (2 * np.arcsin(np.sqrt(a)))

def run_gravity_and_plot(city_csv, shapefile_path, results_csv_path, plot_path, K=64380.06):
    # Load city data with GDP
    cities = pd.read_csv(city_csv)
    cities["GDP"] = pd.to_numeric(cities["GDP"], errors="coerce")
    cities = cities.dropna(subset=["Population", "GDP", "Latitude", "Longitude"]).copy()

    # Calculate flows
    records = []
    for c1, c2 in combinations(cities.to_dict('records'), 2):
        mass1 = c1["Population"] * c1["GDP"]
        mass2 = c2["Population"] * c2["GDP"]
        d = haversine(c1["Latitude"], c1["Longitude"], c2["Latitude"], c2["Longitude"])
        flow = 0 if d <= 0 else K * (mass1 * mass2) / (d**2)
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
    flows_df.to_csv(results_csv_path, index=False)
    print(f"[gdp_gravity_viz] Saved flows to {results_csv_path}")

    # Visualization
    flows_gdf = gpd.GeoDataFrame(
        flows_df,
        geometry=[LineString([(row["lon1"], row["lat1"]), (row["lon2"], row["lat2"])]) for _, row in flows_df.iterrows()],
        crs="EPSG:4326"
    )
    cities_gdf = gpd.GeoDataFrame(
        cities, geometry=gpd.points_from_xy(cities["Longitude"], cities["Latitude"]), crs="EPSG:4326"
    )
    germany_map = gpd.read_file(shapefile_path)
    fig, ax = plt.subplots(figsize=(12, 12))
    germany_map.plot(ax=ax, color="lightgrey", edgecolor="black")
    max_flow = flows_gdf["Flow"].max() if flows_gdf["Flow"].max() > 0 else 1.0
    flows_gdf["width"] = (flows_gdf["Flow"] / max_flow) * 5
    flows_gdf["width"] = flows_gdf["width"].clip(lower=0.2)
    for _, row in flows_gdf.iterrows():
        x, y = row.geometry.xy
        ax.plot(x, y, linewidth=row["width"], color="blue", alpha=0.5)
    cities_gdf.plot(ax=ax, color="red", markersize=20)
    for _, r in cities_gdf.iterrows():
        ax.text(r.geometry.x + 0.05, r.geometry.y + 0.05, r["CityName"], fontsize=6)
    ax.set_title("Gravity Model Flows (Pop×GDP, Distance², K)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"[gdp_gravity_viz] Plot saved to {plot_path}")

if __name__ == "__main__":
    # Example direct usage; main workflow will instead import the function
    run_gravity_and_plot("project_data/german_cities_with_gdp.csv", 
                         "data/germany_shapefile.shp", 
                         "project_data/gravity_flows.csv", 
                         "project_data/gravity_plot.png")
