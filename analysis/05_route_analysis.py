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

# Group by route
route_analysis = operated_flights.groupby(
    ["ORIGIN", "DEST"]
).agg(
    total_flights=("ORIGIN", "count"),
    delayed_flights=("IS_DELAYED", "sum")
).reset_index()

# Calculate delay rate
route_analysis["delay_rate"] = (
    route_analysis["delayed_flights"]
    / route_analysis["total_flights"]
    * 100
)

# Keep routes with at least 100 flights
route_analysis = route_analysis[
    route_analysis["total_flights"] >= 100
]

# Sort by delay rate
route_analysis = route_analysis.sort_values(
    "delay_rate",
    ascending=False
)

# Display top 20 routes
print("========== ROUTE DELAY ANALYSIS ==========")
print("Routes with at least 100 operated flights")
print()

print(
    route_analysis.head(20).to_string(index=False)
)