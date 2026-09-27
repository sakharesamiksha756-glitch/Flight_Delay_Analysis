import pandas as pd

# Load the dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Keep only normal operated flights
operated_flights = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Create a column to identify delayed flights
operated_flights["IS_DELAYED"] = operated_flights["ARR_DELAY"] >= 15

# Group flights by airline
airline_analysis = operated_flights.groupby("OP_UNIQUE_CARRIER").agg(
    total_flights=("OP_UNIQUE_CARRIER", "count"),
    delayed_flights=("IS_DELAYED", "sum")
).reset_index()

# Calculate delay rate
airline_analysis["delay_rate"] = (
    airline_analysis["delayed_flights"]
    / airline_analysis["total_flights"]
    * 100
)

# Sort by delay rate
airline_analysis = airline_analysis.sort_values(
    "delay_rate",
    ascending=False
)

# Display the result
print("========== AIRLINE DELAY ANALYSIS ==========")
print(airline_analysis.to_string(index=False))