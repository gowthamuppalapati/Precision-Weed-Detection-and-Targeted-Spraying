import os
import numpy as np
import rioxarray
import geopandas as gpd
from rasterio.features import shapes
from shapely.geometry import shape

# -----------------------------
# Paths
# -----------------------------
INPUT_RASTER = "outputs/rasters/weed_risk_clean.tif"
OUTPUT_VECTOR = "outputs/vectors/management_zones.geojson"

os.makedirs("outputs/vectors", exist_ok=True)

# -----------------------------
# Load raster
# -----------------------------
print("Loading cleaned weed raster...")
raster = rioxarray.open_rasterio(INPUT_RASTER).squeeze()

data = raster.values
transform = raster.rio.transform()
crs = raster.rio.crs

print("Raster loaded")
print("Shape:", data.shape)

# -----------------------------
# Extract polygons where value == 1
# -----------------------------
print("Converting raster patches to polygons...")

results = []
for geom, value in shapes(data.astype(np.int16), transform=transform):
    if value == 1:
        results.append({
            "geometry": shape(geom),
            "risk": int(value)
        })

if not results:
    raise ValueError("No management zones found in raster.")

gdf = gpd.GeoDataFrame(results, crs=crs)

print("Number of polygons created:", len(gdf))

# -----------------------------
# Save polygons
# -----------------------------
gdf.to_file(OUTPUT_VECTOR, driver="GeoJSON")

print(f"✅ Management zones saved to: {OUTPUT_VECTOR}")