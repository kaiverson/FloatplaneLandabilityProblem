"""
data cleaning and wrangling code to clean the test data
"""

import pandas as pd

df = pd.read_csv('lakes.csv')
print(df)

df['floatplanes'] = 1

apts = pd.read_csv('airports.csv')
print(apts)


def dms_to_decimal(dms):
    parts = dms.split('-')
    degrees, minutes, seconds_direction = parts[0], parts[1], parts[2]
    seconds, direction = seconds_direction[:-1], seconds_direction[-1]

    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600

    # Adjust for direction
    if direction in ['S', 'W']:
        decimal *= -1

    return decimal

apts['Lat'] = apts['ARPLatitude'].apply(dms_to_decimal)
apts['Long'] = apts['ARPLongitude'].apply(dms_to_decimal)


apts['floatplanes'] = apts['Type'].apply(lambda r: 1 if r == "SEAPLANE BASE" else 0)
apts['LakeName'] = apts['FacilityName']

wdf = pd.concat([df[['Lat', 'Long', 'floatplanes', 'LakeName']], apts[['Lat', 'Long', 'floatplanes', "LakeName"]]])

wdf[['Lat', 'Long', 'floatplanes', "LakeName"]].to_csv("cleaned.csv", index=False)

