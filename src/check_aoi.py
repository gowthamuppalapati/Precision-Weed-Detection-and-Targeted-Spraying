import geopandas as gpd

aoi_path = "data/raw/aoi/field_boundary.geojson"

gdf = gpd.read_file(aoi_path)

print(gdf)
print("\nCRS:", gdf.crs)