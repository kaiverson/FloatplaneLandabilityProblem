import pandas as pd
from functions.polygons import is_point_in_polygon
from functions.debugging_tools import stop_watch

@stop_watch
def generate_positive_identification_statistics(outline_df: pd.DataFrame,
                                                marker_df: pd.DataFrame,
                                                verbose: bool = False,
                                                ) -> pd.DataFrame:
    """
    takes the outlines of the lakes and the marker points for each landable lake, checks to see
    that the marker point lies with each polygon, then returns a dataframe of relevant statistics.
    Args:
        verbose: if you want it to print the stats out
        outline_df: the lakes as vertices in a dataframe
        marker_df: the points we want to check

    Returns: a dataframe with the following information:

    Returns the marker df with a new collumn "detected" which shows us each detected point

    """

    unique_polygon_numbers = outline_df['Polygon'].unique()

    known_lakes_considered = 0
    lakes_correctedly_detected = 0

    marker_df['detected'] = 0

    for index, row in marker_df.iterrows():
        # get the lat long of the lake
        lat, lon = row['Lat'], row['Long']
        known_lakes_considered += 1

        for poly_id in unique_polygon_numbers:
            poly = outline_df[outline_df['Polygon'] == poly_id]
            poly_lats = poly['Latitude'].to_list()
            poly_lons = poly['Longitude'].to_list()
            poly_verts = list(zip(poly_lats, poly_lons))

            if is_point_in_polygon(poly_verts, (lat, lon)):
                lakes_correctedly_detected += 1
                marker_df.at[index, 'detected'] = 1  # Set 'detected' flag directly on the original DataFrame
                break

    if verbose:
        print(f'considered {known_lakes_considered} lakes')
        print(f'correctly detected {lakes_correctedly_detected}')
        print(f'{round(100* lakes_correctedly_detected / known_lakes_considered, 2)}% of known lakes detected')

    return marker_df

