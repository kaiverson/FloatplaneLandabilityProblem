import numpy as np
import pandas as pd
import re


def extract_numbers(input_string):
    # regular expression to get all the numbers (thanks chatgpt for generating the expression)
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', input_string)]


def find_polygons(numbers):
    """
    takes a list of lat-lons and extracts the polygons from the list.

    Args:
        numbers: a list of numbers corresponding to the data from gee

    Returns: a list of polygons

    """
    # loop through the numbers
    polygons = []
    polygon = []
    for i in range(0, len(numbers), 2):
        x, y = numbers[i], numbers[i + 1]
        if not polygon or [x, y] != polygon[0]:
            # if you don't have anything in the polygon, or the polygon isn't closed add the point onto the list
            polygon.append([x, y])
        else:
            # now that you ahve all the points close the polygon
            polygon.append(polygon[0])
            polygons.append(polygon)
            polygon = []  # reset the polygon for the next one
    return polygons


def preprocess_polygons(df: pd.DataFrame) -> pd.DataFrame:
    """
    takes a dataframe in the format output by google earth engine and forms it into a dataframe that we can
    work with that's in the format that Kai produced.  It does this by iterating through the rows of the dataframe
    and parsing the strings with a regular expression.

    there is probably a better way to do that though, and arguably we should explore how to vectorize this if we're
    running into performance issues.

    Args:
        df: the dataframe loaded from the .csv file

    Returns: a dataframe with the polygons appropriately processed like this:

    Polygon | Latitude | Longitude
        1       ...         ...      <- this is a point on the first polygon
        1       ...         ...
        ..      ...         ...
        n       ...         ...     <- this is a point on the nth polygon
        n       ...         ...
        ...     ...         ...

    """

    # lists to hold the inevitable data we extract
    latitudes = []
    longitudes = []
    numbering = []

    # get the raw coordinates by parsing the text in the dataframe
    raw_coordinates = sum([extract_numbers(polygon_row['.geo']) for _, polygon_row in df.iterrows()], [])

    # convert those raw coordinates into polygons again
    polygons = find_polygons(raw_coordinates)

    # now loop through the data and build a dataframe
    for i, polygon in enumerate(polygons):
        for lon, lat in polygon:
            numbering.append(i)
            latitudes.append(lat)
            longitudes.append(lon)

    data = {"Latitude": latitudes,
            "Longitude": longitudes,
            "Polygon": numbering}
    return pd.DataFrame(data)


def read_polygons_from_csv(polygons_path, max_polygons=None):
    """
    Read polygons from a CSV file.

    Parameters: 
        polygons_path (str): File path to the CSV file containing polygon data.
        max_polygons (int): The maximum number of polygons to load.

    Returns: 
        numpy.ndarray: Array of polygons, where each polygon is represented as an array of ordered pairs.
    """
    polygons = {}
    df = preprocess_polygons(pd.read_csv(polygons_path))
    df.reset_index()
    polygon_amount = 0

    for index, row in df.iterrows():
        if row['Polygon'] not in polygons.keys():
            polygon_amount += 1
            if max_polygons and polygon_amount > max_polygons:
                break

            polygons[row['Polygon']] = []

        polygons[row['Polygon']].append([row['Latitude'], row['Longitude']])

    for key in polygons.keys():
        polygons[key] = np.array(polygons[key])

    return polygons


def raw_vertices_to_df(polygons: list[list]) -> pd.DataFrame:
    data = {"Polygon": [],
            "Latitude": [],
            "Longitude": []}

    for polygon_number, polygon in enumerate(polygons):
        for latitude, longitude in polygon:
            data["Polygon"].append(polygon_number)
            data["Latitude"].append(latitude)
            data["Longitude"].append(longitude)

    return pd.DataFrame(data, columns=['Polygon', 'Latitude', 'Longitude'])


def export_polygons_from_raw_vertices(filename: str,
                                      polygons: list[list]) -> None:
    data = {"Polygon": [],
            "Latitude": [],
            "Longitude": []}

    for polygon_number, polygon in enumerate(polygons):
        for latitude, longitude in polygon:
            data["Polygon"].append(polygon_number)
            data["Latitude"].append(latitude)
            data["Longitude"].append(longitude)

    df = pd.DataFrame(data, columns=['Polygon', 'Latitude', 'Longitude'])
    df.to_csv(filename, index=False)

    return None
