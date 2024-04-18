import numpy as np
import pandas as pd
"""
takes some _verticies.csv file and removes the polygon that surrounds the roi
the polygon that surrounds the roi is the largest polygon in the file
in the _verticies.csv file, the largest polygon would the be polygon that's id occurs the most
"""

def find_most_common_id_and_remove(filename):
    df = pd.read_csv(filename)
    
    # get the id of the polygon that occurs the most
    surrounding_poly = df['Polygon'].mode()[0]
    print(f"Removing polygon {surrounding_poly} from {filename}")
    df = pd.read_csv(filename)
    df = df[df['Polygon'] != surrounding_poly]
    df.to_csv(filename, index=False)

# if __name__ == "__main__":
#     find_most_common_id_and_remove(filename='lake_pass_1_vertices.csv')