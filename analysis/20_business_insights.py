import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "data/T_ONTIME_REPORTING.csv"

df = pd.read_csv(file_path)

print("Original dataset:", df.shape)


# ============================================================
# 2. KEEP NORMAL OPERATED FLIGHTS
# ============================================================

operated = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0) &
    (df["ARR_DELAY"].notna())
].copy()

print("Operated flights:", len(operated))


# ============================================================
# 3. CREATE DELAY FLAG
# ============================================================

operated["IS_DELAYED"] = (
    operated["ARR_DELAY"] >= 15
).astype(int)


# ============================================================
# 4. OVERALL BUSINESS INSIGHTS
# ============================================================

total_operated = len(operated)

delayed_flights = operated["IS_DELAYED"].sum()

delay_rate = (
    delayed_flights / total_operated
) * 100

average_delay = operated["ARR_DELAY"].mean()

median_delay = operated["ARR_DELAY"].median()


print("\n")
print("=" * 70)
print("                 OVERALL BUSINESS INSIGHTS")
print("=" * 70)

print(f"Total operated flights : {total_operated:,}")
print(f"Delayed flights        : {delayed_flights:,}")
print(f"Overall delay rate     : {delay_rate:.2f}%")
print(f"Average arrival delay  : {average_delay:.2f} minutes")
print(f"Median arrival delay   : {median_delay:.2f} minutes")


# ============================================================
# 5. AIRLINE INSIGHTS
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
    ascending=False
)


print("\n")
print("=" * 70)
print("                 AIRLINE INSIGHTS")
print("=" * 70)

print("\nHighest observed delay rates:")
print(
    airline[
        ["total_flights", "delayed_flights", "delay_rate"]
    ].head(5)
)

print("\nLowest observed delay rates:")
print(
    airline[
        ["total_flights", "delayed_flights", "delay_rate"]
    ].tail(5).sort_values("delay_rate")
)


# ============================================================
# 6. AIRPORT INSIGHTS
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
)


print("\n")
print("=" * 70)
print("                 AIRPORT INSIGHTS")
print("=" * 70)

print("\nAirports with highest observed delay rates:")
print(
    airport[
        ["total_flights", "delayed_flights", "delay_rate"]
    ].head(10)
)


# ============================================================
# 7. ROUTE INSIGHTS
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
)


print("\n")
print("=" * 70)
print("                 ROUTE INSIGHTS")
print("=" * 70)

print("\nRoutes with highest observed delay rates:")

print(
    route[
        ["total_flights", "delayed_flights", "delay_rate"]
    ].head(10)
)


# ============================================================
# 8. TIME-OF-DAY INSIGHTS
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

time_analysis = time_analysis.sort_values(
    "delay_rate",
    ascending=False
)


print("\n")
print("=" * 70)
print("                 TIME-OF-DAY INSIGHTS")
print("=" * 70)

print(
    time_analysis[
        ["total_flights", "delayed_flights", "delay_rate"]
    ]
)


# ============================================================
# 9. DAY-OF-WEEK INSIGHTS
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

day_analysis = day_analysis.sort_values(
    "delay_rate",
    ascending=False
)


print("\n")
print("=" * 70)
print("                 DAY-OF-WEEK INSIGHTS")
print("=" * 70)

print(
    day_analysis[
        ["total_flights", "delayed_flights", "delay_rate"]
    ]
)


# ============================================================
# 10. DELAY CAUSE INSIGHTS
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
    ascending=False
)

total_cause_minutes = cause_summary.sum()

cause_percentage = (
    cause_summary /
    total_cause_minutes
) * 100


cause_table = pd.DataFrame({
    "delay_minutes": cause_summary,
    "percentage": cause_percentage
})


print("\n")
print("=" * 70)
print("                 DELAY CAUSE INSIGHTS")
print("=" * 70)

print(cause_table)


# ============================================================
# 11. KEY BUSINESS FINDINGS
# ============================================================

highest_airline = airline.index[0]
highest_airline_rate = airline.iloc[0]["delay_rate"]

highest_airport = airport.index[0]
highest_airport_rate = airport.iloc[0]["delay_rate"]

highest_route = route.index[0]

highest_time_period = time_analysis.index[0]
highest_time_rate = time_analysis.iloc[0]["delay_rate"]

highest_day = day_analysis.index[0]
highest_day_rate = day_analysis.iloc[0]["delay_rate"]

top_delay_cause = cause_summary.index[0]
top_delay_cause_percentage = cause_percentage.iloc[0]


print("\n")
print("=" * 70)
print("                 KEY BUSINESS FINDINGS")
print("=" * 70)

print(
    f"\n1. Overall observed arrival delay rate: "
    f"{delay_rate:.2f}%"
)

print(
    f"2. Airline with highest observed delay rate "
    f"(minimum 500 flights): {highest_airline} "
    f"({highest_airline_rate:.2f}%)"
)

print(
    f"3. Origin airport with highest observed delay rate "
    f"(minimum 500 flights): {highest_airport} "
    f"({highest_airport_rate:.2f}%)"
)

print(
    f"4. Route with highest observed delay rate "
    f"(minimum 100 flights): "
    f"{highest_route[0]} -> {highest_route[1]}"
)

print(
    f"5. Time period with highest observed delay rate: "
    f"{highest_time_period} ({highest_time_rate:.2f}%)"
)

print(
    f"6. Day with highest observed delay rate: "
    f"{highest_day} ({highest_day_rate:.2f}%)"
)

print(
    f"7. Largest category of cause-attributed delay minutes: "
    f"{top_delay_cause} ({top_delay_cause_percentage:.2f}%)"
)


# ============================================================
# 12. END
# ============================================================

print("\n")
print("=" * 70)
print("              BUSINESS INSIGHTS COMPLETED!")
print("=" * 70)