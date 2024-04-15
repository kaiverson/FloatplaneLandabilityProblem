#####################################################################
# Created by Pat Group Project Team One (Just Kai Iverson for now)
# Implements a naive solution to the float plane landability problem.
# File created on 4-1-2024
#####################################################################

import pandas as pd
import numpy as np
import os
from time import time

from functions.files import *
from functions.polygons import *

from time import time 
  
  
def stop_watch(func): 
    # This tells you how long it took for a function to execute.
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func  


@stop_watch
def main_function(target_meters=500.0, polygons_path='polygons_unprocessed.csv', results_path='results.csv',
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
    # TODO: make code more readable.
    # TODO: make output more readable.
    # TODO: add more polygon information. Min edge, max edge, etc.
    abs_polygons_path = os.path.abspath(polygons_path)
    if not os.path.exists(abs_polygons_path):
        print(f"CSV file '{polygons_path}' not found.")
        return

    polygons = read_polygons_from_csv(polygons_path, max_polygons)
    polygon_results = []


    passed = 0
    failed = 0

    for polygon, vertices in polygons.items():
        solution = has_length_within_polygon_naive(vertices, target_meters, visualize)
        location = average_vertice_location(vertices)

        edge_lengths = edge_lengths_of_polygon(vertices, lat_lon_to_meters(vertices[0]))
        edge_mean = np.mean(edge_lengths)
        edge_std = np.std(edge_lengths)
        perimeter = np.sum(edge_lengths)

        vertices_amount = len(vertices)
        polygon_results.append((int(polygon), location[0], location[1], solution, perimeter))
        if print_info and solution == "Passes":
            print(f"Polygon {polygon:>6.0f}: {solution:<10} Lat,Lon: ({location[0]}, {location[1]}), # vertices: {vertices_amount}, Edge mean: {edge_mean:.3f}, Edge std: {edge_std:.3f}, Perimeter: {perimeter:>10}")
        if solution == 'Fails':
            failed += 1
        else:
            #print(np.array2string(vertices, separator=', '))
            passed += 1



    total = passed + failed
    percent_passed = (100 * passed) / total
    print()
    print(f"Results:")
    print(f"{total} total polygons.")
    print(f"{passed} polygons passed.")
    print(f"{failed} polygons failed.")
    print(f"{percent_passed:.1f}% of the polygons passed.")

    # Write results to CSV file using Pandas
    df = pd.DataFrame(polygon_results, columns=['Polygon', 'Latitude', 'Longitude', 'Result', 'Perimeter'])
    df.to_csv(results_path, index=False)


if __name__ == "__main__":
    main_function(target_meters=500.0, results_path='sucssesful_polygons.csv', visualize=False, max_polygons=None)
