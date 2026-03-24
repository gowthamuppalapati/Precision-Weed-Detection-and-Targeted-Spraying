from pystac_client import Client
import geopandas as gpd

# Load AOI
aoi = gpd.read_file("data/raw/aoi/field_boundary.geojson")

# Convert AOI to GeoJSON format
bbox = aoi.total_bounds  # minx, miny, maxx, maxy

# Connect to STAC
catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-06-01/2023-08-30",
    query={"eo:cloud_cover": {"lt": 20}},
)

items = list(search.get_items())

print(f"Found {len(items)} scenes")

# Print first scene ID
if items:
    print("First scene ID:", items[0].id)