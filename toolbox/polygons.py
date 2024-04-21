import pandas as pd
from toolbox.distance import *


def edge_lengths_of_polygon(vertices, lat_lon_to_meters):
    """
    Calculate the length of the each of the edges of a polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
        lat_lon_to_meters ([float, float]): Conversion rate from lat to meters and from lon to meters.
        
    Returns:
        (numpy.ndarray): length of each edge. Edge n corresponds to vertices n and n+1.
    """
    num_vertices = vertices.shape[0]
    edge_distances = np.zeros(num_vertices)

    for n in range(num_vertices - 1):
        edge_distances[n] = distance_between_vertices(vertices, n, n + 1, lat_lon_to_meters)

    last_edge = distance_between_vertices(vertices, num_vertices - 1, 0, lat_lon_to_meters)

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


def check_diagonal_length(vertices, i, j, target_meters, lat_lon_to_meters):
    """
    Determines if a diagonal is longer than the target distance.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices fo the polygon.
        i (int): index of the first endpoint of the diagonal.
        j (int): index of the second endpoint of the diagonal.
        target_meters (float): the target distance in meters.
        lat_lon_to_meters ([float, float]): Conversion rate from lat to meters and from lon to meters.

    Returns:
        bool: True if diagonal passes, False if diagonal doesn't pass.
    """
    distance = distance_between_vertices(vertices, i, j, lat_lon_to_meters)
    passes = True if distance >= target_meters else False

    return passes


def check_diagonal_path(vertices, i, j):
    """
    Determines if a diagonal has a clear path. Basically a concave detector.
    Warning: this will significantly slow down the code. Consider reducing the amount of vertices in a polygon if it is excessive (> 1000).

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices fo the polygon.
        i (int): Index of the first endpoint of the diagonal.
        j (int): Index of the second endpoint of the diagonal.

    Returns:
        bool: True if diagonal passes, False if diagonal doesn't pass.
    """
    return NotImplementedError()


def is_point_in_polygon(vertices: [tuple], point_coordinates: tuple) -> bool:
    """
    use the raycasting algorithm to check to see if the point is inside the polygon.

    this is a modified version of the explanation from:
    http://www.philliplemons.com/posts/ray-casting-algorithm


    Args:
        vertices: a list of tuples containing the (x,y) coords of each point of the polygon
        point_coordinates: the point we want to check as a tuple

    Returns: true or false depending on whether the polygon contains the point

    """

    # TODO: consider if adding epsilons is necessary for our purposes

    # unpack the point coordinate tuple
    x, y = point_coordinates

    # initialize some stuff
    n = len(vertices)
    inside = False  # start from the standpoint that you're not "inside"
    point_1_x, point_1_y = vertices[0]  # get the first edge from the vertices

    for i in range(n + 1):
        # get the second edge, this counts up 0 - n, then at n + 1 goes back to the first point
        point_2_x, point_2_y = vertices[i % n]

        # check to see if the point is bounded between the y values - that's a requirement for the ray to intersect
        if min(point_1_y, point_2_y) < y <= max(point_1_y, point_2_y):
            # now check to make sure the point is less than the max x-value
            if x<= max(point_1_x, point_2_x):
                if point_1_y != point_2_y:
                    intercept = (y - point_1_y) * (point_2_x - point_1_x) / (point_2_y - point_1_y) + point_1_x

                    if point_1_x == point_2_x or x <= intercept:
                        inside = not inside

        point_1_x, point_1_y = point_2_x, point_2_y

    return inside


def has_length_within_polygon_naive(vertices, target_meters, visualize=False):
    """
    Determines which polygons have a straight line distance of at least target_meters contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        vertices (numpy.ndarray): Array of ordered pairs representing the vertices of the polygon, where each pair is (latitude, longitude).
        target_meters (float): the distance that we are checking for within the polygon
    """
    # TODO: if min_index_offset > num_vertices / 2, polygon should fail. (Think about what this case implies)
    # TODO: if diagonal passes length check, only then perform concave check.
    # TODO: The min_index offset thing needs to treat vertices as a closed loop and not a list.
    # TODO: Make this function readable.
    # TODO: Add edges_checked counter which divided by num_vertices^2 gives a sense of optimization.
    # TODO: Maybe add counter for how many concave checks were made.
    
    conversion = lat_lon_to_meters(vertices[0])

    edge_lengths = edge_lengths_of_polygon(vertices, conversion)
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

            # Question 1: Do we even consider the diagonal?
            if i >= j - min_index_offset:
                continue

            # Question 2: Is the diagonal's length great enough for a float plane to land?
            is_greater_than_target = check_diagonal_length(vertices, i, j, target_meters, conversion)
            if not is_greater_than_target:
                continue

            # NOT IMPLIMENTED. 
            # Question 3: Does the diagonal have a clear path (Doesn't intersect the polygon anywhere)?
            # is_path_clear = check_diagonal_path(vertices, i, j)
            # if not is_path_clear:
            #    continue
            
            # Congratulations, this lake is float plane landable.
            return "Passes"

    # Unfortunately this lake is not float plane landable.
    return "Fails"


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

def find_most_common_id_and_remove(df: pd.DataFrame) -> pd.DataFrame:
    # get the id of the polygon that occurs the most
    surrounding_poly = df['Polygon'].mode()[0]
    return df[df['Polygon'] != surrounding_poly]
