import geopandas as gpd

INPUT_VECTOR = "outputs/vectors/management_zones.geojson"
OUTPUT_VECTOR = "outputs/vectors/management_zones_filtered.geojson"

print("Loading management zones...")
gdf = gpd.read_file(INPUT_VECTOR)

print("Original zones:", len(gdf))

# Reproject to metric CRS for area calculation
gdf_metric = gdf.to_crs("EPSG:32632")  # UTM zone 32N, suitable for much of Germany

# Calculate area in square meters
gdf_metric["area_m2"] = gdf_metric.geometry.area

# Keep only polygons larger than threshold
min_area = 20  # square meters, adjust later if needed
filtered = gdf_metric[gdf_metric["area_m2"] >= min_area].copy()

print("Zones after filtering:", len(filtered))

# Convert back to WGS84 for saving
filtered = filtered.to_crs("EPSG:4326")

filtered.to_file(OUTPUT_VECTOR, driver="GeoJSON")

print(f"✅ Filtered management zones saved to: {OUTPUT_VECTOR}")