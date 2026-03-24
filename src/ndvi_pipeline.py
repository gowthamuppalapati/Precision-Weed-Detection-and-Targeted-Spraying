import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import stackstac
import rioxarray
from pystac_client import Client
import planetary_computer

# -----------------------------
# Paths
# -----------------------------
AOI_PATH = "data/raw/aoi/field_boundary.geojson"
OUTPUT_RASTER = "outputs/rasters/ndvi.tif"
OUTPUT_PLOT = "outputs/plots/ndvi_map.png"

os.makedirs("outputs/rasters", exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)

# -----------------------------
# Load AOI
# -----------------------------
aoi = gpd.read_file(AOI_PATH)

if aoi.crs is None:
    raise ValueError("AOI has no CRS defined.")

aoi = aoi.to_crs("EPSG:4326")
bbox = tuple(map(float, aoi.total_bounds))

print("AOI loaded successfully.")
print("AOI bounds:", bbox)

# -----------------------------
# Search Sentinel-2
# -----------------------------
catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-06-01/2023-08-30",
    query={"eo:cloud_cover": {"lt": 20}},
)

items = list(search.items())

if not items:
    raise ValueError("No Sentinel-2 scenes found. Try a wider date range or higher cloud threshold.")

print(f"Found {len(items)} Sentinel-2 scenes.")
item = items[0]
print("Using scene:", item.id)
print("Scene date:", item.datetime)

signed_item = planetary_computer.sign(item)
print("Available assets:", list(signed_item.assets.keys()))

# -----------------------------
# Resolve projection metadata
# -----------------------------
scene_epsg = item.properties.get("proj:epsg")

if scene_epsg is None:
    # Fallback to asset-level projection metadata
    scene_epsg = signed_item.assets["B04"].extra_fields.get("proj:epsg")

if scene_epsg is None:
    # Last-resort fallback from tile ID in your current example
    # T12... corresponds to UTM zone 12N -> EPSG:32612
    scene_epsg = 32612
    print("Warning: proj:epsg missing at item and asset level; using fallback EPSG 32612.")

print("Scene EPSG:", scene_epsg)

# -----------------------------
# Reproject AOI to scene CRS
# -----------------------------
aoi_proj = aoi.to_crs(epsg=scene_epsg)

# -----------------------------
# Load B04 and B08 in native/proper projected CRS
# -----------------------------
# Do NOT force epsg=4326 with resolution=10, because 10 would mean 10 degrees.
data = stackstac.stack(
    [signed_item],
    assets=["B04", "B08"],
    epsg=scene_epsg,
    resolution=10,
)

print("Stack loaded.")
print(data)

# -----------------------------
# Select scene and compute bands
# -----------------------------
red = data.sel(band="B04").isel(time=0).astype("float32").compute()
nir = data.sel(band="B08").isel(time=0).astype("float32").compute()

print("Original Red shape:", red.shape)
print("Original NIR shape:", nir.shape)

# -----------------------------
# Ensure CRS is attached
# -----------------------------
red = red.rio.write_crs(f"EPSG:{scene_epsg}")
nir = nir.rio.write_crs(f"EPSG:{scene_epsg}")

# -----------------------------
# Clip to AOI
# -----------------------------
red_clip = red.rio.clip(aoi_proj.geometry, aoi_proj.crs, drop=True)
nir_clip = nir.rio.clip(aoi_proj.geometry, aoi_proj.crs, drop=True)

print("Clipped Red shape:", red_clip.shape)
print("Clipped NIR shape:", nir_clip.shape)

# -----------------------------
# NDVI
# -----------------------------
ndvi = (nir_clip - red_clip) / (nir_clip + red_clip)
ndvi = ndvi.where(np.isfinite(ndvi))

if np.isnan(ndvi.values).all():
    raise ValueError("NDVI contains only NaN values after clipping. Check AOI location and scene coverage.")

print("NDVI calculated.")
print("NDVI shape:", ndvi.shape)
print("NDVI min:", float(ndvi.min(skipna=True).values))
print("NDVI max:", float(ndvi.max(skipna=True).values))

# -----------------------------
# Save raster
# -----------------------------
print("Saving raster to:", os.path.abspath(OUTPUT_RASTER))
ndvi.rio.to_raster(OUTPUT_RASTER)
print(f"NDVI raster saved to: {OUTPUT_RASTER}")

# -----------------------------
# Plot
# -----------------------------
print("Saving plot to:", os.path.abspath(OUTPUT_PLOT))

plt.figure(figsize=(10, 8))
ndvi.plot(cmap="RdYlGn")
plt.title("NDVI Map")
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=300)
plt.show()

print(f"NDVI plot saved to: {OUTPUT_PLOT}")