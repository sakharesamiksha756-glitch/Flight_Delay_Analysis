import pandas as pd

# Load the flight dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Display first 5 rows
print("FIRST 5 ROWS:")
print(df.head())

# Display number of rows and columns
print("\nDATASET SHAPE:")
print(df.shape)

# Display all column names
print("\nCOLUMN NAMES:")
print(df.columns)

# Display information about the dataset
print("\nDATASET INFORMATION:")
print(df.info())
