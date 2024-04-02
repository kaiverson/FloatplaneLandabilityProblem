#####################################################################
# Created by Pat Group Project Team One (Just Kai Iverson for now)
# Implements a naive solution to the float plane landability problem.
# File created on 4-1-2024
#####################################################################

import pandas as pd
import numpy as np
import os


def read_polygons_from_csv(polygons_path):
    """
    Read polygons from a CSV file.

    Parameters: 
        polygons_path (str): File path to the CSV file containing polygon data.

    Returns: 
        numpy.ndarray: Array of polygons, where each polygon is represented as an array of ordered pairs.
    """
    polygons = {}
    df = pd.read_csv(polygons_path)
    df.reset_index()

    for index, row in df.iterrows():
        if row['Polygon'] not in polygons.keys():
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
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
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
        edge_distances[n] = distance_between_points_on_earth(vertices, n, n+1)

    last_edge = distance_between_points_on_earth(vertices, num_vertices-1, 0)

    edge_distances[num_vertices-1] = last_edge
    return edge_distances


def has_length_within_polygon_naive(vertices, target_miles, visualize=False):
    """
    Determines which polygons have a straight line distance of at least target_miles contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        vertices (numpy.ndarray): 
        target_miles (float): the distance that we are checking for within the polygon
    """
    # If vertices are too close together in the vertices list,
    # their distance will never be larger than the longest edge length.
    edge_lengths = edge_distances_of_polygon(vertices)
    longest_edge_length = edge_lengths.max()
    min_index_offset = target_miles // longest_edge_length
    if visualize: print("min_index_offset:", int(min_index_offset))
    if min_index_offset == 0:
        return 'Passes*         *May have only passed due to low resolution'
    
    solution = "Fails"
    num_vertices = vertices.shape[0]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i + min_index_offset >= j:
                if visualize: print(" ~", end='')
                continue
            distance = distance_between_points_on_earth(vertices, i, j)
            passes = True if distance >= target_miles else False
            if visualize: print(f" {1 if passes else 0}", end='')
            solution = "Passes" if passes == True else solution
            if passes and not visualize: return solution 
        if visualize: print()


    return solution




def main_function(target_miles=0.5, polygons_path='polygons.csv', results_path='results.csv', visualize=False):
    """
    Determines which polygons have a straight line distance of at least target_miles contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        target_miles (float): the distance that we are checking for within the polygon
        polygons_path (str): file path to file containing csv polygons. 
        results_path (str): file path to file containing the results.
    """
    abs_polygons_path = os.path.abspath(polygons_path)
    if not os.path.exists(abs_polygons_path):
        print(f"CSV file '{polygons_path}' not found.")
        return
    
    polygons = read_polygons_from_csv(polygons_path)
    polygon_amount = len(polygons.keys())
    print()
    print(f"{polygon_amount} polygon{'' if polygon_amount==1 else 's'} loaded from {polygons_path}.")
    print(f"Searching polygon vertices for straight line distance greater than {target_miles} miles...")
    print()

    for polygon, vertices in polygons.items():
        solution_for_polygon = has_length_within_polygon_naive(vertices, target_miles, visualize)
        print(f"Polygon {int(polygon)}:", solution_for_polygon)


if __name__ == "__main__":
    main_function(target_miles=18.2, visualize=True)


