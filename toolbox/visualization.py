"""
This script needs to provide a function to join together the .csv files containing polygon vertices
and load them into a single map, together with the cleaned landable lakes data from Toby's work.
"""
import pandas as pd
import folium



def map_lakes(outline_df: pd.DataFrame, marker_df: pd.DataFrame, map_file_name: str = "map.html") -> None:
    """
    takes in a dataframe with the polygons as well as a source of marker dataframe and saves a
    single file
    Args:
        outline_df: the dataframe containing the points you wish to outline
        marker_df: the dataframe containing the points you wish to save as markers

    Returns:

    """

    mean_lat = outline_df['Latitude'].mean()
    mean_lon = outline_df['Longitude'].mean()
    map = folium.Map(location=[mean_lat, mean_lon], zoom_start=3)

    unique_polygon_numbers = outline_df['Polygon'].unique()
    outlines_fg = folium.FeatureGroup(name=f'Detected Lake Polygons')
    correct_markers = folium.FeatureGroup(name=f"Correctly Marked Lakes")
    incorrect_markers = folium.FeatureGroup(name="Incorrectly Labeled Lakes")

    # Add a satellite layer
    satellite = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite Image',
        overlay=True
    )

    satellite.add_to(map)

    for poly_id in unique_polygon_numbers:
        poly = outline_df[outline_df['Polygon'] == poly_id]

        lats = poly['Latitude'].to_list()
        lons = poly['Longitude'].to_list()

        folium.PolyLine([[lat, lon] for lat, lon in zip(lats, lons)], color="red", weight=2.5, opacity=1).add_to(outlines_fg)

    for index, row in marker_df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Long']],
            popup=f"Known Landable Lake:  {row['LakeName']}",
            icon=folium.Icon(color='green' if row["detected"] else "red")
        ).add_to(correct_markers if row['detected'] else incorrect_markers)



    outlines_fg.add_to(map)
    correct_markers.add_to(map)
    incorrect_markers.add_to(map)

    folium.LayerControl().add_to(map)

    map.save(map_file_name)

