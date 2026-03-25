import geopandas as gpd
import rioxarray
import numpy as np

# Load zones
zones = gpd.read_file("outputs/vectors/management_zones_filtered.geojson")

# Load NDVI raster
ndvi = rioxarray.open_rasterio("outputs/rasters/ndvi.tif").squeeze()

# Function to extract mean NDVI inside polygon
def get_mean_ndvi(geom):
    try:
        clipped = ndvi.rio.clip([geom], all_touched=True)
        vals = clipped.values.astype(float)
        # Mask nodata values (common nodata: -9999, nan)
        vals[vals == -9999] = np.nan
        return float(np.nanmean(vals))
    except:
        return None

print("Calculating NDVI per zone...")

zones["mean_ndvi"] = zones.geometry.apply(get_mean_ndvi)

# Assign priority
def assign_priority(val):
    if val is None or np.isnan(val):
        return "Unknown"
    elif val < 0.2:
        return "High"
    elif val < 0.4:
        return "Medium"
    else:
        return "Low"

zones["priority"] = zones["mean_ndvi"].apply(assign_priority)

# ── Fix: drop any extra geometry columns before saving ──────────────────────
active_geom = zones.geometry.name
extra_geoms = [c for c in zones.select_dtypes(include="geometry").columns
               if c != active_geom]
zones = zones.drop(columns=extra_geoms)
# ────────────────────────────────────────────────────────────────────────────

# Save
zones.to_file("outputs/vectors/spray_priority_zones.geojson", driver="GeoJSON")

print("✅ Spray priority zones created")