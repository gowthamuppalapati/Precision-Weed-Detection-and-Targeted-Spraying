import os
import numpy as np
import rioxarray
from scipy import ndimage
import xarray as xr   # ✅ FIX

# -----------------------------
# Paths
# -----------------------------
INPUT_PATH = "outputs/rasters/weed_risk.tif"
OUTPUT_PATH = "outputs/rasters/weed_risk_clean.tif"

os.makedirs("outputs/rasters", exist_ok=True)

# -----------------------------
# Load raw weed map
# -----------------------------
print("Loading weed risk raster...")
weed = rioxarray.open_rasterio(INPUT_PATH).squeeze()

print("Raster loaded")
print("Shape:", weed.shape)

# Convert to numpy array
weed_array = weed.values

# -----------------------------
# Label connected patches
# -----------------------------
print("Labelling connected components...")

structure = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

labeled_array, num_features = ndimage.label(weed_array == 1, structure=structure)

print("Number of detected patches:", num_features)

# -----------------------------
# Remove very small patches
# -----------------------------
min_pixels = 20   # you can adjust this later

cleaned = np.zeros_like(weed_array)

for label_id in range(1, num_features + 1):
    patch = labeled_array == label_id
    patch_size = np.sum(patch)

    if patch_size >= min_pixels:
        cleaned[patch] = 1

print("Noise removal complete")

# -----------------------------
# Save cleaned raster
# -----------------------------
cleaned_da = xr.DataArray(
    cleaned,
    coords=weed.coords,
    dims=weed.dims
)

cleaned_da.rio.write_crs(weed.rio.crs, inplace=True)
cleaned_da.rio.to_raster(OUTPUT_PATH)

print(f"✅ Cleaned weed map saved to: {OUTPUT_PATH}")
