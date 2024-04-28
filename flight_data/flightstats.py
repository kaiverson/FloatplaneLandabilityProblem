"""
Code to take and generate a histogram and also explain what is happening.
-pat
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# load the flights file

df = pd.read_csv('flights.csv')

print(df)

print('initial data')
print(df.head())

print('minimums for each category:')
print(df.min())

print('max for each category')
print(df.max())


print('now make a histogram, filter for lakes that are the median size or smaller')
sizes = df['Dest_sqkm']
reduced_sizes = sizes[sizes < sizes.median()]

# Plotting the histogram
reduced_sizes.hist(bins=30, alpha=0.7, color='blue', edgecolor='black')

# Adding titles and labels
plt.title(f'Lake Area Histogram for lakes smaller than {sizes.median(): 2.1f} sqkm')
plt.xlabel('Lake Area')
plt.ylabel('Frequency')

# Display the plot
plt.savefig("flightshist.png")
