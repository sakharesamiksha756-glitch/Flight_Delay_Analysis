# ✈️ Flight Delay Analysis & Operational Insights

## 📌 Project Overview

This project analyzes historical U.S. flight data to identify flight delay patterns, airline performance, airport performance, route-level risks, and major causes of flight delays.

The project combines **Python, Pandas, SQL, SQLite, Streamlit, Data Visualization, and Machine Learning** to transform raw flight data into meaningful operational insights.

---

## 🎯 Project Objectives

The main objectives of this project are:

- Analyze overall flight performance.
- Identify airlines with higher and lower delay rates.
- Analyze airport-level delay patterns.
- Identify high-risk flight routes.
- Understand major causes of flight delays.
- Analyze delay patterns by day and time.
- Build a machine learning model to predict flight delays.
- Create an interactive dashboard for exploring the results.

---

## 📊 Dataset

The project uses historical U.S. flight data stored in:

`data/T_ONTIME_REPORTING.csv`

### Dataset size

- Total records: **539,747**
- Total columns: **25**

The dataset contains information about:

- Flight date
- Airline
- Flight number
- Origin airport
- Destination airport
- Scheduled departure time
- Actual departure time
- Departure delay
- Scheduled arrival time
- Actual arrival time
- Arrival delay
- Cancellation
- Diversion
- Distance
- Delay causes

---

## 🛠️ Technologies Used

### Programming & Analysis

- Python
- Pandas
- NumPy

### Database & SQL

- SQLite
- SQL

### Visualization

- Matplotlib
- Streamlit

### Machine Learning

- Scikit-learn
- Logistic Regression
- Random Forest

### Development Tools

- VS Code
- Jupyter Notebook
- Git
- GitHub

---

# 📁 Project Structure

```text
Flight_Delay_Analysis/
│
├── analysis/
│   ├── flight_delay_random_forest.pkl
│   ├── 21_create_visualizations.py
│   └── ...
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── T_ONTIME_REPORTING.csv
│
├── images/
│   ├── 01_overall_delay_rate.png
│   ├── 02_airline_delay_rate.png
│   ├── 03_airport_delay_rate.png
│   ├── 04_route_delay_rate.png
│   ├── 05_time_of_day_delay_rate.png
│   ├── 06_day_of_week_delay_rate.png
│   ├── 07_delay_causes.png
│   └── 08_arrival_delay_distribution.png
│
├── notebooks/
│
├── sql/
│   ├── flight_delay.db
│   └── 01_flight_analysis.sql
│
└── README.md