import sys
import os
import pandas as pd
from polygons import find_most_common_id_and_remove

# to access the main.py file which is in the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from main import main_function


def csv_loop():
    csv_list = ['lakes_csv/lake_boundaries_1.csv', 'lakes_csv/lake_boundaries_2.csv', 'lakes_csv/lake_boundaries_3.csv',
                'lakes_csv/lake_boundaries_4.csv']
    results_list = ['lake_pass_1.csv', 'lake_pass_2.csv', 'lake_pass_3.csv', 'lake_pass_4.csv']

    for i, j in zip(csv_list, results_list):
        main_function(target_meters=500.0, polygons_path=i, results_path=j,
                      visualize=False, max_polygons=None, print_info=True, export_successful=True)

    for i in results_list:
        df = pd.read_csv(i)
        df = find_most_common_id_and_remove(df)
        df.to_csv(i, index=False)

if __name__ == "__main__":
    csv_loop()
