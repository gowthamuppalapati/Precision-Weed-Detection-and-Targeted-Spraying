import os
import rioxarray
import numpy as np
import xarray as xr   # ✅ FIX

# -----------------------------
# Paths
# -----------------------------
NDVI_PATH = "outputs/rasters/ndvi.tif"
OUTPUT_PATH = "outputs/rasters/weed_risk.tif"

os.makedirs("outputs/rasters", exist_ok=True)

# -----------------------------
# Load NDVI
# -----------------------------
print("Loading NDVI raster...")
ndvi = rioxarray.open_rasterio(NDVI_PATH).squeeze()

print("NDVI loaded successfully")
print("NDVI shape:", ndvi.shape)

# -----------------------------
# Weed logic
# -----------------------------
print("Applying weed detection logic...")

weed_risk = np.where(ndvi < 0.4, 1, 0)

print("Weed risk classification done")

# -----------------------------
# Convert to DataArray (FIXED)
# -----------------------------
weed_risk_da = xr.DataArray(
    weed_risk,
    coords=ndvi.coords,
    dims=ndvi.dims
)

weed_risk_da.rio.write_crs(ndvi.rio.crs, inplace=True)
weed_risk_da.rio.to_raster(OUTPUT_PATH)

print(f"✅ Weed suspicion map saved at: {OUTPUT_PATH}")