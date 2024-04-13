import folium
import pandas as pd

from functions.files import preprocess_polygons
from functions.files import read_polygons_from_csv

df = pd.read_csv("../lakes_csv/lake_boundaries_1.csv")
df = preprocess_polygons(df)

mean_lat = df['Latitude'].mean()
mean_lon = df['Longitude'].mean()
map = folium.Map(location=[mean_lat, mean_lon], zoom_start=3)

unique_polygon_numbers = df['Polygon'].unique()

for poly_id in unique_polygon_numbers:
    poly = df[df['Polygon'] == poly_id]

    lats = poly['Latitude'].to_list()
    lons = poly['Longitude'].to_list()

    fg = folium.FeatureGroup(name=f'Poly {poly_id}')
    folium.PolyLine([[lat, lon] for lat, lon in zip(lats, lons)], color="red", weight=2.5, opacity=1).add_to(fg)
    fg.add_to(map)


folium.LayerControl().add_to(map)
map.save("map.html")
