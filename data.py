import pandas as pd

file_path = "dataset.csv"
df = pd.read_csv(file_path)

print(df.head())

print(df.info())

print(df.isnull().sum())
