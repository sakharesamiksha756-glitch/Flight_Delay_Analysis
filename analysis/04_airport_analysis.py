import pandas as pd

# Load the dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Keep normal operated flights
operated_flights = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Identify delayed flights
operated_flights["IS_DELAYED"] = operated_flights["ARR_DELAY"] >= 15

# Group by departure airport
airport_analysis = operated_flights.groupby("ORIGIN").agg(
    total_flights=("ORIGIN", "count"),
    delayed_flights=("IS_DELAYED", "sum")
).reset_index()

# Calculate delay rate
airport_analysis["delay_rate"] = (
    airport_analysis["delayed_flights"]
    / airport_analysis["total_flights"]
    * 100
)

# Keep airports with at least 500 flights
airport_analysis = airport_analysis[
    airport_analysis["total_flights"] >= 500
]

# Sort by delay rate
airport_analysis = airport_analysis.sort_values(
    "delay_rate",
    ascending=False
)

# Display results
print("========== AIRPORT DELAY ANALYSIS ==========")
print("Airports with at least 500 operated flights")
print()

print(
    airport_analysis.head(20).to_string(index=False)
)