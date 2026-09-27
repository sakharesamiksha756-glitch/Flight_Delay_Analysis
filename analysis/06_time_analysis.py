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

# Convert scheduled departure time into a 4-digit string
operated_flights["DEP_HOUR"] = (
    operated_flights["CRS_DEP_TIME"]
    .astype(int)
    .astype(str)
    .str.zfill(4)
    .str[:2]
    .astype(int)
)

# Create time-of-day categories
def get_time_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

operated_flights["TIME_PERIOD"] = operated_flights["DEP_HOUR"].apply(
    get_time_period
)

# Group by time period
time_analysis = operated_flights.groupby("TIME_PERIOD").agg(
    total_flights=("TIME_PERIOD", "count"),
    delayed_flights=("IS_DELAYED", "sum")
).reset_index()

# Calculate delay rate
time_analysis["delay_rate"] = (
    time_analysis["delayed_flights"]
    / time_analysis["total_flights"]
    * 100
)

# Sort by delay rate
time_analysis = time_analysis.sort_values(
    "delay_rate",
    ascending=False
)

print("========== TIME-OF-DAY DELAY ANALYSIS ==========")
print()

print(
    time_analysis.to_string(index=False)
)