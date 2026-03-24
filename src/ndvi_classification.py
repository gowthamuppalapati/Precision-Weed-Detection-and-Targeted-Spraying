import os
import numpy as np
import rioxarray
import matplotlib.pyplot as plt
import xarray as xr

# Paths
NDVI_PATH = "outputs/rasters/ndvi.tif"
OUTPUT_CLASS = "outputs/rasters/ndvi_classes.tif"
OUTPUT_PLOT = "outputs/plots/ndvi_classes.png"

os.makedirs("outputs/rasters", exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)

# Load NDVI
ndvi = rioxarray.open_rasterio(NDVI_PATH).squeeze()

print("NDVI loaded")

# Classification
classes = np.zeros_like(ndvi)

classes = np.where(ndvi < 0.2, 1, classes)   # Bare soil
classes = np.where((ndvi >= 0.2) & (ndvi < 0.4), 2, classes)  # Weak
classes = np.where((ndvi >= 0.4) & (ndvi < 0.6), 3, classes)  # Moderate
classes = np.where(ndvi >= 0.6, 4, classes)  # Healthy

print("Classification done")

# Save raster

# Create DataArray
classified = xr.DataArray(classes, coords=ndvi.coords, dims=ndvi.dims)

# Write CRS
classified.rio.write_crs(ndvi.rio.crs, inplace=True)

# Save raster
classified.rio.to_raster(OUTPUT_CLASS)

print(f"Saved classification raster: {OUTPUT_CLASS}")

# Plot
plt.figure(figsize=(10, 8))
plt.imshow(classes, cmap="viridis")
plt.title("NDVI Classification")
plt.colorbar(label="Class")
plt.axis("off")
plt.savefig(OUTPUT_PLOT, dpi=300)
plt.show()

print(f"Saved classification plot: {OUTPUT_PLOT}")