import rioxarray
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Path to NDVI raster
# -----------------------------
NDVI_PATH = "outputs/rasters/ndvi.tif"

# -----------------------------
# Load NDVI raster
# -----------------------------
ndvi = rioxarray.open_rasterio(NDVI_PATH)

# Remove band dimension (if exists)
ndvi = ndvi.squeeze()

print("NDVI loaded successfully.")

# -----------------------------
# Validate NDVI values
# -----------------------------
ndvi_min = float(ndvi.min().values)
ndvi_max = float(ndvi.max().values)

print("NDVI min:", ndvi_min)
print("NDVI max:", ndvi_max)

# -----------------------------
# Check for invalid values
# -----------------------------
if ndvi_min < -1 or ndvi_max > 1:
    print("⚠️ Warning: NDVI values out of expected range (-1 to 1)")
else:
    print("✅ NDVI values are within expected range")

# -----------------------------
# Plot Histogram
# -----------------------------
plt.figure(figsize=(8, 5))
ndvi.plot.hist(bins=50)
plt.title("NDVI Distribution")
plt.xlabel("NDVI Value")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -----------------------------
# Optional: Show NDVI map again
# -----------------------------
plt.figure(figsize=(8, 6))
ndvi.plot(cmap="RdYlGn")
plt.title("NDVI Map (Validation View)")
plt.axis("off")
plt.tight_layout()
plt.show()

print("Validation completed.")