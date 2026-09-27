import pandas as pd

# Load the dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# Delay cause columns
delay_columns = [
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

# Replace missing delay-cause values with 0
df[delay_columns] = df[delay_columns].fillna(0)

# Calculate total delay minutes for each cause
cause_totals = df[delay_columns].sum().reset_index()

# Rename columns
cause_totals.columns = ["delay_cause", "total_delay_minutes"]

# Sort from highest to lowest
cause_totals = cause_totals.sort_values(
    "total_delay_minutes",
    ascending=False
)

# Calculate percentage of total cause-attributed delay
total_delay_minutes = cause_totals["total_delay_minutes"].sum()

cause_totals["percentage"] = (
    cause_totals["total_delay_minutes"]
    / total_delay_minutes
    * 100
)

print("========== DELAY CAUSE ANALYSIS ==========")
print()

print(cause_totals.to_string(index=False))