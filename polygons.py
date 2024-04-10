import numpy as np

from distance import *


def edge_lengths_of_polygon(vertices):
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
        edge_distances[n] = distance_between_vertices(vertices, n, n + 1)

    last_edge = distance_between_vertices(vertices, num_vertices - 1, 0)

    edge_distances[num_vertices - 1] = last_edge
    return edge_distances


def perimeter_length(edge_lengths):
    """
    Calculates the perimeter length of a polygon. BEWARE OF THE COASTLINE PARADOX.

    Args:
        edge_lengths (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
    """
    perimeter = np.sum(edge_lengths)
    return perimeter


def edge_length_standard_deviation(edge_lengths):
    """
    Calculate the standard deviation of the edge lengths of a polygon.

    Parameters:
        edge_lengths (numpy.ndarray): Array of ordered pairs representing the edge lengths of a polygon.

    Returns:
        float: Standard deviation of the edge lengths.
    """
    standard_deviation = np.std(edge_lengths)
    return standard_deviation


def average_vertice_location(vertices):
    """
    Calculates the average location of the vertices. 
    
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


def has_length_within_polygon_naive(vertices, target_meters, visualize=False):
    """
    Determines which polygons have a straight line distance of at least target_meters contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
        target_meters (float): the distance that we are checking for within the polygon
    """
    # TODO: if min_index_offset > num_vertices / 2, polygon should fail.
    # TODO: if diagonal passes length check, only then perform concave check.
    # TODO: The min_index offset thing needs to treat vertices as a closed loop and not a list.
    # TODO: Make this function readable.
    # TODO: Add edges_checked counter which divided by num_vertices^2 gives a sense of optimization.
    # TODO: Maybe add counter for how many concave checks were made.
    edge_lengths = edge_lengths_of_polygon(vertices)
    longest_edge_length = edge_lengths.max()
    min_index_offset = target_meters // longest_edge_length
    if visualize:
        print("min_index_offset:", int(min_index_offset))
    if min_index_offset == 0:
        return 'Passes*'

    solution = "Fails"
    num_vertices = vertices.shape[0]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i >= j - min_index_offset:
                if visualize:
                    print(" ~", end='')
                continue
            distance = distance_between_vertices(vertices, i, j)
            passes = True if distance >= target_meters else False
            if visualize: print(f" {1 if passes else 0}", end='')
            solution = "Passes" if passes is True else solution
            if passes and not visualize:
                return solution
        if visualize:
            print()

    

    return solution