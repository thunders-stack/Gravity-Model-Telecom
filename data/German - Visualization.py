# 4. Create GeoDataFrames for plotting
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

# 5. Plot on Germany map
germany_map = gpd.read_file("de_shp/de.shp")
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

ax.set_title("Gravity Model Flows (Pop×GDP, Distance², K=64380.06)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.show()