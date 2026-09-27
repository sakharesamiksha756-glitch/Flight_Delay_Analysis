import pandas as pd

# Load the flight dataset
df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

# 1. Total number of flights
total_flights = len(df)

# 2. Cancelled flights
cancelled_flights = (df["CANCELLED"] == 1).sum()

# 3. Diverted flights
diverted_flights = (df["DIVERTED"] == 1).sum()

# Flights used for normal arrival analysis
# We exclude cancelled and diverted flights
operated_flights = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
]

# 4. Delayed flights: arrival delay >= 15 minutes
delayed_flights = (operated_flights["ARR_DELAY"] >= 15).sum()

# 5. On-time / under 15 minutes
on_time_flights = (operated_flights["ARR_DELAY"] < 15).sum()

# 6. Delay percentage
delay_rate = (delayed_flights / len(operated_flights)) * 100


# Display results
print("========== BASIC FLIGHT ANALYSIS ==========")

print("Total Flights:", total_flights)
print("Cancelled Flights:", cancelled_flights)
print("Diverted Flights:", diverted_flights)
print("Operated Flights:", len(operated_flights))
print("Delayed Flights (15+ min):", delayed_flights)
print("On-Time Flights (<15 min):", on_time_flights)

print(f"Arrival Delay Rate: {delay_rate:.2f}%")