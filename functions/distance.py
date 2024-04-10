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


def euclidean(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate the euclidean distance between two points.

    Parameters:
        x1, y1 (float): (x, y) coordinates of point 1.
        x2, y2 (float): (x, y) coordinates of point 2.

    Returns:
        float: represents the distance between the two points. 
    """
    dx: float = x2 - x1
    dy: float = y2 - y1
    distance: float = np.sqrt((dx * dx) + (dy * dy))
    return distance


def distance_between_vertices(vertices: np.ndarray, 
                              index1: int, index2: int, 
                              distance=haversine) -> float:
    """
    Calculate the distance between two points using some notion of distance.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon.
        index1 (int): Index of the first point.
        index2 (int): Index of the second point.
        distance (function): function used as the notion of distance. Arguments are ordered pairs point1 and point2. Default is the haversine function.

    Returns:
        float: Distance between the two points in miles.
    """
    x1, y1 = vertices[index1]
    x2, y2 = vertices[index2]
    distance = distance(x1, y1, x2, y2)
    return distance