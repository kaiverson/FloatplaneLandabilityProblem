import sys
import os

##to access the main.py file which is in the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from main import main_function

## importation error "ModuleNotFoundError: No module named 'main'"
## I tried to fix this by adding main.py sys path but it still did not work
## for now just I just copy and pasted the csv_loop function into the main.py file

def csv_loop():
    csv_list = ['lakes_csv\lake_boundaries_1.csv', 'lakes_csv/lake_boundaries_2.csv', 'lakes_csv/lake_boundaries_3.csv', 'lakes_csv/lake_boundaries_4.csv']
    results_list = ['lake_results_1.csv', 'lake_results_2.csv', 'lake_results_3.csv', 'lake_results_4.csv']
    
    for i,j in zip(csv_list, results_list):
        main_function(target_meters=500.0, polygons_path= i, results_path= j,
                  visualize=False, max_polygons=None, print_info=True)

if __name__ == "__main__":
    csv_loop()    