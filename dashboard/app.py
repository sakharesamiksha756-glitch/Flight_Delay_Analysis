import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Flight Delay Analysis",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sql" / "flight_delay.db"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        FL_DATE,
        OP_UNIQUE_CARRIER,
        ORIGIN,
        DEST,
        CRS_DEP_TIME,
        DEP_TIME,
        DEP_DELAY,
        CRS_ARR_TIME,
        ARR_TIME,
        ARR_DELAY,
        CANCELLED,
        DIVERTED,
        DISTANCE,
        CARRIER_DELAY,
        WEATHER_DELAY,
        NAS_DELAY,
        SECURITY_DELAY,
        LATE_AIRCRAFT_DELAY
    FROM flights
    """

    data = pd.read_sql_query(query, conn)

    conn.close()

    return data


df = load_data()


# ============================================================
# DATA TYPE CONVERSION
# ============================================================

numeric_columns = [
    "ARR_DELAY",
    "DEP_DELAY",
    "CANCELLED",
    "DIVERTED",
    "DISTANCE",
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Missing delay causes are treated as zero

delay_columns = [
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

for column in delay_columns:

    df[column] = df[column].fillna(0)


# ============================================================
# OPERATIONAL FLIGHTS
# ============================================================

# Cancelled and diverted flights are excluded
# from operational delay analysis.

operated = df[
    (df["CANCELLED"] == 0) &
    (df["DIVERTED"] == 0)
].copy()


# ============================================================
# DELAY FLAG
# ============================================================

# A flight is considered delayed when arrival delay
# is 15 minutes or more.

operated["IS_DELAYED"] = (
    operated["ARR_DELAY"] >= 15
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title(
    "✈️ Flight Delay Analysis & Operational Insights"
)

st.markdown(
    """
    This dashboard analyzes historical U.S. flight data to identify
    flight delay patterns, airline performance, airport performance,
    route risks, and major delay causes.
    """
)


# ============================================================
# OVERALL KPI CALCULATIONS
# ============================================================

total_flights = len(df)

operated_flights = len(operated)

cancelled_flights = int(
    (df["CANCELLED"] == 1).sum()
)

diverted_flights = int(
    (df["DIVERTED"] == 1).sum()
)

delayed_flights = int(
    operated["IS_DELAYED"].sum()
)

delay_rate = (
    delayed_flights / operated_flights * 100
    if operated_flights > 0
    else 0
)


# ============================================================
# OVERALL FLIGHT PERFORMANCE
# ============================================================

st.subheader("📊 Overall Flight Performance")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Total Flights",
    f"{total_flights:,}"
)


col2.metric(
    "Operated Flights",
    f"{operated_flights:,}"
)


col3.metric(
    "Cancelled Flights",
    f"{cancelled_flights:,}"
)


col4.metric(
    "Delayed Flights",
    f"{delayed_flights:,}"
)


col5.metric(
    "Delay Rate",
    f"{delay_rate:.2f}%"
)


st.caption(
    f"Diverted flights excluded from operational delay analysis: "
    f"{diverted_flights:,}"
)


st.divider()


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("🔎 Filters")

st.sidebar.write(
    "Use the filter below to explore airline-specific performance."
)


carriers = sorted(
    operated["OP_UNIQUE_CARRIER"]
    .dropna()
    .unique()
)


selected_carriers = st.sidebar.multiselect(
    "Select Airline",
    carriers,
    default=carriers
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = operated[
    operated["OP_UNIQUE_CARRIER"].isin(
        selected_carriers
    )
].copy()


# ============================================================
# FILTERED KPI CALCULATIONS
# ============================================================

filtered_flights = len(filtered_df)

filtered_delayed = int(
    filtered_df["IS_DELAYED"].sum()
)

filtered_delay_rate = (
    filtered_delayed /
    filtered_flights *
    100
    if filtered_flights > 0
    else 0
)


# ============================================================
# FILTERED RESULTS
# ============================================================

st.subheader("✈️ Filtered Results")


f1, f2, f3 = st.columns(3)


f1.metric(
    "Selected Flights",
    f"{filtered_flights:,}"
)


f2.metric(
    "Delayed Flights",
    f"{filtered_delayed:,}"
)


f3.metric(
    "Delay Rate",
    f"{filtered_delay_rate:.2f}%"
)


st.divider()


# ============================================================
# AIRLINE DELAY PERFORMANCE
# ============================================================

st.subheader("🛫 Airline Delay Performance")


if len(filtered_df) > 0:

    airline_analysis = (
        filtered_df
        .groupby("OP_UNIQUE_CARRIER")
        .agg(
            Flights=("IS_DELAYED", "count"),
            Delayed_Flights=("IS_DELAYED", "sum"),
            Average_Arrival_Delay=("ARR_DELAY", "mean")
        )
        .reset_index()
    )


    airline_analysis["Delay_Rate"] = (
        airline_analysis["Delayed_Flights"]
        /
        airline_analysis["Flights"]
        *
        100
    )


    airline_analysis = airline_analysis.sort_values(
        "Delay_Rate",
        ascending=False
    )


    airline_display = airline_analysis.copy()


    airline_display["Average_Arrival_Delay"] = (
        airline_display["Average_Arrival_Delay"]
        .round(2)
    )


    airline_display["Delay_Rate"] = (
        airline_display["Delay_Rate"]
        .round(2)
    )


    st.dataframe(
        airline_display,
        width="stretch",
        hide_index=True
    )


    st.bar_chart(
        airline_analysis.set_index(
            "OP_UNIQUE_CARRIER"
        )["Delay_Rate"]
    )

else:

    st.info(
        "Please select at least one airline from the sidebar."
    )


st.divider()


# ============================================================
# AIRPORT DELAY PERFORMANCE
# ============================================================

st.subheader("🛬 Airport Delay Performance")


if len(filtered_df) > 0:

    airport_analysis = (
        filtered_df
        .groupby("ORIGIN")
        .agg(
            Flights=("IS_DELAYED", "count"),
            Delayed_Flights=("IS_DELAYED", "sum"),
            Average_Arrival_Delay=("ARR_DELAY", "mean")
        )
        .reset_index()
    )


    airport_analysis["Delay_Rate"] = (
        airport_analysis["Delayed_Flights"]
        /
        airport_analysis["Flights"]
        *
        100
    )


    # Only airports with at least 500 flights

    airport_analysis = airport_analysis[
        airport_analysis["Flights"] >= 500
    ]


    airport_analysis = airport_analysis.sort_values(
        "Delay_Rate",
        ascending=False
    )


    airport_display = airport_analysis.copy()


    airport_display["Average_Arrival_Delay"] = (
        airport_display["Average_Arrival_Delay"]
        .round(2)
    )


    airport_display["Delay_Rate"] = (
        airport_display["Delay_Rate"]
        .round(2)
    )


    st.dataframe(
        airport_display.head(20),
        width="stretch",
        hide_index=True
    )


    st.bar_chart(
        airport_analysis
        .head(15)
        .set_index("ORIGIN")["Delay_Rate"]
    )

else:

    st.info(
        "No airport data available for the selected airlines."
    )


st.divider()


# ============================================================
# ROUTE DELAY PERFORMANCE
# ============================================================

st.subheader("🗺️ Route Delay Performance")


if len(filtered_df) > 0:

    route_analysis = (
        filtered_df
        .groupby(
            ["ORIGIN", "DEST"]
        )
        .agg(
            Flights=("IS_DELAYED", "count"),
            Delayed_Flights=("IS_DELAYED", "sum"),
            Average_Arrival_Delay=("ARR_DELAY", "mean")
        )
        .reset_index()
    )


    route_analysis["Delay_Rate"] = (
        route_analysis["Delayed_Flights"]
        /
        route_analysis["Flights"]
        *
        100
    )


    # Only routes with at least 100 flights

    route_analysis = route_analysis[
        route_analysis["Flights"] >= 100
    ]


    route_analysis = route_analysis.sort_values(
        "Delay_Rate",
        ascending=False
    )


    route_display = route_analysis.copy()


    route_display["Average_Arrival_Delay"] = (
        route_display["Average_Arrival_Delay"]
        .round(2)
    )


    route_display["Delay_Rate"] = (
        route_display["Delay_Rate"]
        .round(2)
    )


    st.dataframe(
        route_display.head(20),
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No route data available for the selected airlines."
    )


st.divider()


# ============================================================
# MAJOR DELAY CAUSES
# ============================================================

st.subheader("⚠️ Major Delay Causes")


if len(filtered_df) > 0:

    delay_causes = {

        "Carrier":
            filtered_df["CARRIER_DELAY"].sum(),

        "Late Aircraft":
            filtered_df["LATE_AIRCRAFT_DELAY"].sum(),

        "NAS":
            filtered_df["NAS_DELAY"].sum(),

        "Weather":
            filtered_df["WEATHER_DELAY"].sum(),

        "Security":
            filtered_df["SECURITY_DELAY"].sum()
    }


    delay_causes_df = pd.DataFrame(
        list(delay_causes.items()),
        columns=[
            "Cause",
            "Delay_Minutes"
        ]
    )


    total_cause_delay = (
        delay_causes_df["Delay_Minutes"].sum()
    )


    if total_cause_delay > 0:

        delay_causes_df["Percentage"] = (
            delay_causes_df["Delay_Minutes"]
            /
            total_cause_delay
            *
            100
        )

    else:

        delay_causes_df["Percentage"] = 0


    delay_causes_df = (
        delay_causes_df
        .sort_values(
            "Percentage",
            ascending=False
        )
    )


    delay_causes_display = (
        delay_causes_df.copy()
    )


    delay_causes_display["Delay_Minutes"] = (
        delay_causes_display["Delay_Minutes"]
        .round(0)
        .astype(int)
    )


    delay_causes_display["Percentage"] = (
        delay_causes_display["Percentage"]
        .round(2)
    )


    # Percentage chart

    st.bar_chart(
        delay_causes_df.set_index(
            "Cause"
        )["Percentage"]
    )


    # Detailed table

    st.dataframe(
        delay_causes_display[
            [
                "Cause",
                "Delay_Minutes",
                "Percentage"
            ]
        ],
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No delay-cause data available for the selected airlines."
    )


st.divider()


# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader("📄 Data Preview")


st.caption(
    "First 100 operational flight records from the selected airlines."
)


preview_columns = [
    "FL_DATE",
    "OP_UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_DEP_TIME",
    "DEP_TIME",
    "DEP_DELAY",
    "CRS_ARR_TIME",
    "ARR_TIME",
    "ARR_DELAY",
    "CANCELLED",
    "DIVERTED",
    "DISTANCE"
]


st.dataframe(
    filtered_df[
        preview_columns
    ].head(100),
    width="stretch",
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.caption(
    "Flight Delay Analysis Project | "
    "Python • SQL • SQLite • Pandas • Streamlit • Machine Learning"
)