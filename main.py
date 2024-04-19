#####################################################################
# Created by Pat Group Project Team One (Just Kai Iverson for now)
# Implements a naive solution to the float plane landability problem.
# File created on 4-1-2024
#####################################################################


import os
import pandas as pd
from functions.files import *
from functions.polygons import *
from functions.visualization import map_lakes
from functions.statistics import generate_positive_identification_statistics
from functions.debugging_tools import stop_watch



@stop_watch
def main_function(target_meters=500.0,
                  polygons_path='polygons_unprocessed.csv',
                  results_path=None,  # use this to export the results to .csv
                  visualize=False,  # use this to visualize the algorithm (not working yet)
                  max_polygons=None,
                  print_info=False,
                  export_successful=False) -> pd.DataFrame:
    """
    Determines which polygons have a straight line distance of at least target_miles contained within them.
    Assumes that polygon vertices represent lattitudes and longitudes. Distances based on haversine formula.
    THIS IS A NAIVE SOLUTION. It ISN'T accurate for concave polygons. For example: the case of a thin 'S' shaped polygon.

    Parameters:
        export_successful: flag to tell the algorithm to export the successful vertices
        target_meters (float): the distance that we are checking for within the polygon
        polygons_path (str): file path to file containing csv polygons. 
        results_path (str): file path to file containing the results.
        visualize (bool): If True, the algorithm will be visualized.
        max_polygons (int): The maximum number of polygons to load.
        print_info (bool): If True, print the information on each of the polygons; otherwise, only write them to the results file.

    return:
        the successful polygons in a dataframe
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
    passing_polygons = []

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
            print(
                f"Polygon {polygon:>6.0f}: {solution:<10} Lat,Lon: ({location[0]}, {location[1]}), # vertices: {vertices_amount}, Edge mean: {edge_mean:.3f}, Edge std: {edge_std:.3f}, Perimeter: {perimeter:>10}")
        if solution == 'Fails':
            failed += 1
        else:
            # print(np.array2string(vertices, separator=', '))
            passing_polygons.append(vertices)
            passed += 1

    total = passed + failed
    percent_passed = (100 * passed) / total

    if print_info:
        # if you're going to print everything out, do so
        print()
        print(f"Results:")
        print(f"{total} total polygons.")
        print(f"{passed} polygons passed.")
        print(f"{failed} polygons failed.")
        print(f"{percent_passed:.1f}% of the polygons passed.")

    # Write results to CSV file using Pandas
    df = pd.DataFrame(polygon_results, columns=['Polygon', 'Latitude', 'Longitude', 'Result', 'Perimeter'])

    if results_path is not None:
        # if you've turned on results path send that to .csv
        df.to_csv(results_path, index=False)

    if export_successful and results_path:
        # if you've turned on export successful and specified a path, export those
        vertices_file_name = f"{os.path.splitext(results_path)[0]}_vertices.csv"
        export_polygons_from_raw_vertices(filename=vertices_file_name, polygons=passing_polygons)

    # convert the raw vertices to a df and return that
    return find_most_common_id_and_remove(raw_vertices_to_df(passing_polygons))


if __name__ == "__main__":
    """
    The main function here should be where we fit together all the pieces of our model.  This is called the "pipe and
    filter architecture"
    
    I went ahead and refactored everything so that the model produces a list of dataframes of successful polygons, then
    concats those together, visualizes them, and checks to see how many points we got right with our algorithm.
    """
    # TODO:  Refactor some of this code to be inside abstracted functions
    # TODO:  Create Diagram for Pipe-Filter Architectural Flow of Code


    csv_list = ['lakes_csv/lake_boundaries_1.csv', 'lakes_csv/lake_boundaries_2.csv', 'lakes_csv/lake_boundaries_3.csv',
                'lakes_csv/lake_boundaries_4.csv']

    successful_polygons = [main_function(polygons_path=csv_file) for csv_file in csv_list]

    # make all the polygon indices unique by adding the length of the previous df to the polygon
    index_counter = 1
    for df in successful_polygons:
        df['Polygon'] = df['Polygon'] + index_counter
        index_counter = index_counter + df["Polygon"].max()

    # put all of these together and calculate the min and max lat-lons
    df = pd.concat(successful_polygons)

    # now load the source of truth,
    lake_truth = pd.read_csv('flight_data/cleaned.csv')
    lake_truth = lake_truth[lake_truth['floatplanes'] == 1]  # we don't care about runways

    """
    we need to filter out places that aren't in our ROI
    """
    matSuROI = [
        (-151.6970688287938, 60.90480020426519),
        (-151.3489595751618, 61.00629812504111),
        (-151.1459775803294, 61.04351337219632),
        (-150.9369163348004, 61.19936156775925),
        (-150.6092949437964, 61.27478397462557),
        (-150.4866081744711, 61.24217854425234),
        (-149.9790927356937, 61.23316377103141),
        (-149.8644558219648, 61.35567989288409),
        (-149.7988576878899, 61.39628094061301),
        (-149.6061035585755, 61.49071772290527),
        (-149.2577295764331, 61.48164025046362),
        (-148.9007510082246, 63.38768837583029),
        (-151.0072124599679, 63.06933025031949),
        (-153.8934978076406, 62.50953235888112),
        (-151.6970688287938, 60.90480020426519)
    ]
    matSuROI = [(lat, lon) for lon, lat in matSuROI]  # reverse this because gee expects it the other way
    lake_truth['roi'] = lake_truth.apply(lambda r: is_point_in_polygon(matSuROI, (r["Lat"], r['Long'])), axis='columns')
    lake_truth = lake_truth[lake_truth['roi']]



    # now we need to check each point in the source of truth data and see if it's bounded by one of the polygons
    lake_truth = generate_positive_identification_statistics(df, lake_truth, verbose=True)
    lake_truth.to_csv('detected_lakes.csv', columns=['Lat', "Long", "LakeName", "detected"], index=False)

    # now send all this to the map_lakes function to generate an html file
    map_lakes(outline_df=df, marker_df=lake_truth)

