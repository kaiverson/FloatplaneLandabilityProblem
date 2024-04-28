"""
by pat

this code was convenience code to convert from degrees to radians
"""

import numpy as np
from sklearn.metrics.pairwise import haversine_distances as hd
from math import radians

lat1s, lon1s = np.radians(np.linspace(0, 90, 3600)).tolist(), np.radians(np.linspace(0, 90, 3600)).tolist()
lat2s, lon2s = np.radians(np.linspace(90, 0, 3600)).tolist(), np.radians(np.linspace(90, 0, 3600)).tolist()


coord1s = zip(lat1s, lon1s)
coord2s = zip(lat2s, lon2s)

hds = [hd([x, y]) for x, y in zip(coord1s, coord2s)]

print(hds)