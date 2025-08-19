# Load city data
cities = pd.read_csv("german_cities_with_gdp.csv")
cities["GDP"] = pd.to_numeric(cities["GDP"], errors="coerce")
cities = cities.dropna(subset=["Population", "GDP", "Latitude", "Longitude"]).copy()

# Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    φ1, φ2 = np.radians(lat1), np.radians(lat2)
    Δφ = φ2 - φ1
    Δλ = np.radians(lon2 - lon1)
    a = np.sin(Δφ / 2)**2 + np.cos(φ1) * np.cos(φ2) * np.sin(Δλ / 2)**2
    return R * (2 * np.arcsin(np.sqrt(a)))

# Compute gravity flows with distance squared and K = 64380.06
K = 64380.06
records = []
for c1, c2 in combinations(cities.to_dict('records'), 2):
    mass1 = c1["Population"] * c1["GDP"]
    mass2 = c2["Population"] * c2["GDP"]
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

# Create GeoDataFrames for plotting (Remove the code below if you do not wish to visualize the data)
flows_gdf = gpd.GeoDataFrame(
    flows_df,
    geometry=[
        LineString([
            (row["lon1"], row["lat1"]),
            (row["lon2"], row["lat2"])
        ])
        for _, row in flows_df.iterrows()
    ],
    crs="EPSG:4326"
)
cities_gdf = gpd.GeoDataFrame(
    cities,
    geometry=gpd.points_from_xy(cities["Longitude"], cities["Latitude"]),
    crs="EPSG:4326"
)

# Plot on Germany map
germany_map = gpd.read_file("path/to/shp/file")
fig, ax = plt.subplots(figsize=(12, 12))
germany_map.plot(ax=ax, color="lightgrey", edgecolor="black")

# Scale line widths
max_flow = flows_gdf["Flow"].max() if flows_gdf["Flow"].max() > 0 else 1.0
flows_gdf["width"] = (flows_gdf["Flow"] / max_flow) * 5
flows_gdf["width"] = flows_gdf["width"].clip(lower=0.2)  # min width

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
plt.show()