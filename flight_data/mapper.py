import os

import folium
import pandas as pd




df = pd.read_csv("../sucssesful_polygons_vertices.csv")

mean_lat = df['Latitude'].mean()
mean_lon = df['Longitude'].mean()
map = folium.Map(location=[mean_lat, mean_lon], zoom_start=3)

unique_polygon_numbers = df['Polygon'].unique()
unique_polygon_numbers = unique_polygon_numbers[0:100]

for poly_id in unique_polygon_numbers:
    poly = df[df['Polygon'] == poly_id]

    lats = poly['Latitude'].to_list()
    lons = poly['Longitude'].to_list()


    fg = folium.FeatureGroup(name=f'Poly {poly_id}')
    folium.PolyLine([[lat, lon] for lat, lon in zip(lats, lons)], color="red", weight=2.5, opacity=1).add_to(fg)
    fg.add_to(map)


folium.LayerControl().add_to(map)
map.save("map.html")
