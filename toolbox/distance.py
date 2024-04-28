"""
This code contains the functions that calculate various distance metrics.  Written by kai

"""

import numpy as np


def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
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

    radius_of_earth_meters = 6371000.0
    
    distance = radius_of_earth_meters * c
    return distance


def euclidean(x1: float, y1: float, x2: float, y2: float, conversion) -> float:
    """
    Calculate the euclidean distance between two points.

    Parameters:
        x1, y1 (float): (x, y) coordinates of point 1.
        x2, y2 (float): (x, y) coordinates of point 2.
        conversion: Conversion rate to squish dx and dy.

    Returns:
        float: represents the distance between the two points. 
    """
    dx: float = (x2 - x1) * conversion[0]
    dy: float = (y2 - y1) * conversion[1]
    distance: float = np.sqrt((dx * dx) + (dy * dy))
    return distance


def lat_lon_to_meters(point, epsilon=0.0001):
    """
    Calculates the conversion rate from 1 degree lat to meters and 1 degree lon to meters for the local area.
    Note that lat should be the same number no matter where on earth it is calculated.

    Parameters:
        point (numpy.ndarray): A lattitude and longitude.
        epsilon (float): A small number. The smaller, the more precise the calculation.

    Returns: 
        numpy.ndarray: The conversion rates.
    """
    # TODO: just calculate the percise limit.
    dmeter_dlat = 111_120.0 # haversine(point[0], point[1], point[0] + epsilon, point[1]) / epsilon     # Partial derivative of meters with respect to lattitude.
    dmeter_dlon = 111_319.488 * np.cos(np.deg2rad(point[0])) # haversine(point[0], point[1], point[0], point[1] + epsilon) / epsilon     # Partial derivative of meters with respect to longitude.
    conversion_rate = np.array([dmeter_dlat, dmeter_dlon])
    return conversion_rate


def distance_between_vertices(vertices: np.ndarray, 
                              index1: int, index2: int,
                              lat_lon_to_meters) -> float:
    """
    Calculate the distance between two points using some notion of distance.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon.
        index1 (int): Index of the first point.
        index2 (int): Index of the second point.
        lat_lon_to_meters ([float, float]): The conversion rate from lat to meters and from lon to meters.

    Returns:
        float: Distance between the two points in miles.
    """
    x1, y1 = vertices[index1]
    x2, y2 = vertices[index2]
    distance = euclidean(x1, y1, x2, y2, lat_lon_to_meters)
    # distance = haversine(x1, y1, x2, y2)             This is slightly over twice as slow.
    return distance