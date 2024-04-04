#####################################################################
# Created by Pat Group Project Team One (Just Kai Iverson for now)
# Implements a naive solution to the float plane landability problem.
# File created on 4-1-2024
#####################################################################

import pandas as pd
import numpy as np
import os
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
        x, y = numbers[i], numbers[i+1]
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


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Parameters:
        lat1, lon1, lat2, lon2: Latitude and longitude of the two points

    Returns:
        float: Distance between the two points in miles
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    radius_of_earth_miles = 3958.8
    distance = radius_of_earth_miles * c
    return distance


def distance_between_points_on_earth(vertices, index1, index2):
    """
    Calculate the distance between two points on Earth represented by their longitude and latitude coordinates.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
        index1 (int): Index of the first point.
        index2 (int): Index of the second point.

    Returns:
        float: Distance between the two points in miles.
    """
    lat1, lon1 = vertices[index1]
    lat2, lon2 = vertices[index2]
    distance = haversine(lat1, lon1, lat2, lon2)
    return distance


def edge_distances_of_polygon(vertices):
    """
    Calculate the length of the each of the edges of a polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).

    Returns:
        (numpy.ndarray): length of each edge. Edge n corresponds to vertices n and n+1.
    """
    num_vertices = vertices.shape[0]
    edge_distances = np.zeros(num_vertices)

    for n in range(num_vertices - 1):
        edge_distances[n] = distance_between_points_on_earth(vertices, n, n + 1)

    last_edge = distance_between_points_on_earth(vertices, num_vertices - 1, 0)

    edge_distances[num_vertices - 1] = last_edge
    return edge_distances


def edge_length_standard_deviation(vertices):
    """
    Calculate the standard deviation of the edge lengths of a polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).

    Returns:
        float: Standard deviation of the edge lengths.
    """
    edge_lengths = edge_distances_of_polygon(vertices)
    return np.std(edge_lengths)


def compute_vertice_average(vertices):
    """
    Calculates the average of all of the vertices. 
    
    Args:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).

    Returns:
        tuple: A tuple containing the average latitude and average longitude.        
    """
    latitudes = vertices[:, 0]
    longitudes = vertices[:, 1]

    avg_latitude = np.mean(latitudes)
    avg_longitude = np.mean(longitudes)

    return avg_latitude, avg_longitude


def perimeter_length(vertices):
    """
    Calculates the perimeter length of a polygon.

    Args:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
    """
    edge_lengths = edge_distances_of_polygon(vertices)
    perimeter = np.sum(edge_lengths)
    return perimeter


def has_length_within_polygon_naive(vertices, target_miles, visualize=False):
    """
    Determines which polygons have a straight line distance of at least target_miles contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
        target_miles (float): the distance that we are checking for within the polygon
    """
    # If vertices are too close together in the vertices list,
    # their distance will never be larger than the longest edge length.
    edge_lengths = edge_distances_of_polygon(vertices)
    longest_edge_length = edge_lengths.max()
    min_index_offset = target_miles // longest_edge_length
    if visualize:
        print("min_index_offset:", int(min_index_offset))
    if min_index_offset == 0:
        return 'Passes*'

    solution = "Fails"
    num_vertices = vertices.shape[0]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i + min_index_offset >= j:
                if visualize:
                    print(" ~", end='')
                continue
            distance = distance_between_points_on_earth(vertices, i, j)
            passes = True if distance >= target_miles else False
            if visualize: print(f" {1 if passes else 0}", end='')
            solution = "Passes" if passes is True else solution
            if passes and not visualize:
                return solution
        if visualize:
            print()

    return solution


def main_function(target_miles=0.5, polygons_path='polygons_unprocessed.csv', results_path='results.csv',
                  visualize=False, max_polygons=None, print_info=True):
    """
    Determines which polygons have a straight line distance of at least target_miles contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        target_miles (float): the distance that we are checking for within the polygon
        polygons_path (str): file path to file containing csv polygons. 
        results_path (str): file path to file containing the results.
        visualize (bool): If True, the algorithm will be visualized.
        max_polygons (int): The maximum number of polygons to load.
        print_info (bool): If True, print the information on each of the polygons; otherwise, only write them to the results file.
    """
    abs_polygons_path = os.path.abspath(polygons_path)
    if not os.path.exists(abs_polygons_path):
        print(f"CSV file '{polygons_path}' not found.")
        return

    polygons = read_polygons_from_csv(polygons_path, max_polygons)
    polygon_results = []

    passed = 0
    failed = 0

    for polygon, vertices in polygons.items():
        solution = has_length_within_polygon_naive(vertices, target_miles, visualize)
        location = compute_vertice_average(vertices)
        perimeter = perimeter_length(vertices)
        vertices_amount = len(vertices)
        polygon_results.append((int(polygon), location[0], location[1], solution, perimeter))
        edge_std = edge_length_standard_deviation(vertices)
        if print_info:
            print(f"Polygon {polygon:>6}: {solution:<10} Lat,Lon: ({location[0]}, {location[1]}), # vertices: {vertices_amount}, Edge std: {edge_std}, Perimeter: {perimeter:>10}")
        if solution == 'Fails':
            failed += 1
        else:
            passed += 1



    total = passed + failed
    percent_passed = (100 * passed) / total
    print()
    print(f"Results:")
    print(f"{total} total polygons.")
    print(f"{passed:>10} polygons passed.")
    print(f"{failed:>10} polygons failed.")
    print(f"{percent_passed:.1f}% of the polygons passed.")

    # Write results to CSV file using Pandas
    df = pd.DataFrame(polygon_results, columns=['Polygon', 'Latitude', 'Longitude', 'Result', 'Perimeter'])
    df.to_csv(results_path, index=False)


if __name__ == "__main__":
    main_function(target_miles=0.310686, visualize=False, max_polygons=40)
