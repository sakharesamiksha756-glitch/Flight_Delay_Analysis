import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "data/T_ONTIME_REPORTING.csv"

df = pd.read_csv(file_path)

print("Dataset loaded:", df.shape)


# ============================================================
# 2. CREATE IMAGES FOLDER
# ============================================================

images_folder = "images"

os.makedirs(images_folder, exist_ok=True)


# ============================================================
# 3. KEEP NORMAL OPERATED FLIGHTS
# ============================================================

operated = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

operated["IS_DELAYED"] = (
    operated["ARR_DELAY"] >= 15
).astype(int)


# ============================================================
# 4. OVERALL DELAY RATE
# ============================================================

total_flights = len(operated)

delayed_flights = operated["IS_DELAYED"].sum()

on_time_flights = total_flights - delayed_flights

labels = [
    "Delayed (15+ min)",
    "Under 15 min"
]

values = [
    delayed_flights,
    on_time_flights
]

plt.figure(figsize=(8, 6))

plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Flight Delay Overview")

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "01_overall_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 01_overall_delay_rate.png")


# ============================================================
# 5. AIRLINE DELAY RATE
# ============================================================

airline = (
    operated
    .groupby("OP_UNIQUE_CARRIER")
    .agg(
        total_flights=("IS_DELAYED", "size"),
        delayed_flights=("IS_DELAYED", "sum")
    )
)

airline["delay_rate"] = (
    airline["delayed_flights"] /
    airline["total_flights"] * 100
)

airline = airline[
    airline["total_flights"] >= 500
].sort_values(
    "delay_rate",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    airline.index,
    airline["delay_rate"]
)

plt.xlabel("Delay Rate (%)")

plt.ylabel("Airline")

plt.title(
    "Observed Flight Delay Rate by Airline"
)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "02_airline_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 02_airline_delay_rate.png")


# ============================================================
# 6. TOP AIRPORTS BY DELAY RATE
# ============================================================

airport = (
    operated
    .groupby("ORIGIN")
    .agg(
        total_flights=("IS_DELAYED", "size"),
        delayed_flights=("IS_DELAYED", "sum")
    )
)

airport["delay_rate"] = (
    airport["delayed_flights"] /
    airport["total_flights"] * 100
)

airport = airport[
    airport["total_flights"] >= 500
].sort_values(
    "delay_rate",
    ascending=False
).head(10)

airport = airport.sort_values(
    "delay_rate",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    airport.index,
    airport["delay_rate"]
)

plt.xlabel("Delay Rate (%)")

plt.ylabel("Origin Airport")

plt.title(
    "Top 10 Origin Airports by Observed Delay Rate"
)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "03_airport_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 03_airport_delay_rate.png")


# ============================================================
# 7. TOP ROUTES BY DELAY RATE
# ============================================================

route = (
    operated
    .groupby(["ORIGIN", "DEST"])
    .agg(
        total_flights=("IS_DELAYED", "size"),
        delayed_flights=("IS_DELAYED", "sum")
    )
)

route["delay_rate"] = (
    route["delayed_flights"] /
    route["total_flights"] * 100
)

route = route[
    route["total_flights"] >= 100
].sort_values(
    "delay_rate",
    ascending=False
).head(10)

route["route"] = (
    route.index.get_level_values("ORIGIN")
    + " → " +
    route.index.get_level_values("DEST")
)

route = route.sort_values(
    "delay_rate",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    route["route"],
    route["delay_rate"]
)

plt.xlabel("Delay Rate (%)")

plt.ylabel("Route")

plt.title(
    "Top 10 Routes by Observed Delay Rate"
)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "04_route_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 04_route_delay_rate.png")


# ============================================================
# 8. TIME-OF-DAY DELAY RATE
# ============================================================

operated["DEP_HOUR"] = (
    operated["CRS_DEP_TIME"] // 100
).astype(int)


def get_time_period(hour):

    if 5 <= hour <= 11:
        return "Morning"

    elif 12 <= hour <= 16:
        return "Afternoon"

    elif 17 <= hour <= 20:
        return "Evening"

    else:
        return "Night"


operated["TIME_PERIOD"] = operated[
    "DEP_HOUR"
].apply(get_time_period)


time_analysis = (
    operated
    .groupby("TIME_PERIOD")
    .agg(
        total_flights=("IS_DELAYED", "size"),
        delayed_flights=("IS_DELAYED", "sum")
    )
)

time_analysis["delay_rate"] = (
    time_analysis["delayed_flights"] /
    time_analysis["total_flights"] * 100
)

time_order = [
    "Morning",
    "Afternoon",
    "Evening",
    "Night"
]

time_analysis = time_analysis.reindex(
    time_order
)

plt.figure(figsize=(9, 6))

plt.bar(
    time_analysis.index,
    time_analysis["delay_rate"]
)

plt.xlabel("Time Period")

plt.ylabel("Delay Rate (%)")

plt.title(
    "Observed Delay Rate by Time of Day"
)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "05_time_of_day_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 05_time_of_day_delay_rate.png")


# ============================================================
# 9. DAY-OF-WEEK DELAY RATE
# ============================================================

operated["FL_DATE"] = pd.to_datetime(
    operated["FL_DATE"],
    format="mixed"
)

operated["DAY_NAME"] = operated[
    "FL_DATE"
].dt.day_name()


day_analysis = (
    operated
    .groupby("DAY_NAME")
    .agg(
        total_flights=("IS_DELAYED", "size"),
        delayed_flights=("IS_DELAYED", "sum")
    )
)

day_analysis["delay_rate"] = (
    day_analysis["delayed_flights"] /
    day_analysis["total_flights"] * 100
)

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_analysis = day_analysis.reindex(
    day_order
)

plt.figure(figsize=(10, 6))

plt.bar(
    day_analysis.index,
    day_analysis["delay_rate"]
)

plt.xlabel("Day of Week")

plt.ylabel("Delay Rate (%)")

plt.title(
    "Observed Delay Rate by Day of Week"
)

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "06_day_of_week_delay_rate.png"),
    dpi=300
)

plt.close()

print("Created: 06_day_of_week_delay_rate.png")


# ============================================================
# 10. DELAY CAUSES
# ============================================================

cause_columns = [
    "CARRIER_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "NAS_DELAY",
    "WEATHER_DELAY",
    "SECURITY_DELAY"
]

cause_totals = {}

for column in cause_columns:

    cause_totals[column] = operated[
        column
    ].fillna(0).sum()


cause_summary = pd.Series(
    cause_totals
).sort_values(
    ascending=True
)


plt.figure(figsize=(10, 6))

plt.barh(
    cause_summary.index,
    cause_summary.values
)

plt.xlabel("Total Delay Minutes")

plt.ylabel("Delay Cause")

plt.title(
    "Delay Minutes by Cause"
)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "07_delay_causes.png"),
    dpi=300
)

plt.close()

print("Created: 07_delay_causes.png")


# ============================================================
# 11. ARRIVAL DELAY DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    operated["ARR_DELAY"],
    bins=100
)

plt.xlabel("Arrival Delay (minutes)")

plt.ylabel("Number of Flights")

plt.title(
    "Distribution of Arrival Delays"
)

plt.xlim(-60, 180)

plt.tight_layout()

plt.savefig(
    os.path.join(images_folder, "08_arrival_delay_distribution.png"),
    dpi=300
)

plt.close()

print("Created: 08_arrival_delay_distribution.png")


# ============================================================
# 12. FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("              VISUALIZATIONS COMPLETED!")
print("=" * 70)

print("\nCharts saved inside:")
print("images/")

print("\nFiles created:")

print("01_overall_delay_rate.png")
print("02_airline_delay_rate.png")
print("03_airport_delay_rate.png")
print("04_route_delay_rate.png")
print("05_time_of_day_delay_rate.png")
print("06_day_of_week_delay_rate.png")
print("07_delay_causes.png")
print("08_arrival_delay_distribution.png")

print("\nAll charts have been saved successfully!")