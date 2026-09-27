import pandas as pd

# Load the dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Convert flight date to datetime
df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

# Keep normal operated flights
operated_flights = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

# Identify delayed flights
operated_flights["IS_DELAYED"] = operated_flights["ARR_DELAY"] >= 15

# Create day-of-week column
operated_flights["DAY_OF_WEEK"] = operated_flights["FL_DATE"].dt.day_name()

# Group by day
day_analysis = operated_flights.groupby("DAY_OF_WEEK").agg(
    total_flights=("DAY_OF_WEEK", "count"),
    delayed_flights=("IS_DELAYED", "sum")
).reset_index()

# Calculate delay rate
day_analysis["delay_rate"] = (
    day_analysis["delayed_flights"]
    / day_analysis["total_flights"]
    * 100
)

# Put days in normal order
day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_analysis["DAY_OF_WEEK"] = pd.Categorical(
    day_analysis["DAY_OF_WEEK"],
    categories=day_order,
    ordered=True
)

day_analysis = day_analysis.sort_values("DAY_OF_WEEK")

print("========== DAY-OF-WEEK DELAY ANALYSIS ==========")
print()

print(day_analysis.to_string(index=False))