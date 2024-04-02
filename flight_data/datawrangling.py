import pandas as pd

df = pd.read_csv('lakes.csv')
print(df)

df[['Lat', 'Long']].to_csv("cleaned.csv", index=False)

