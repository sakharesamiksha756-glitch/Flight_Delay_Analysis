\# ✈️ Flight Delay Prediction and Operational Insights



\## 📌 Project Overview



This project analyzes historical flight data to understand flight delays, cancellations, delay patterns, and operational factors.



The project combines \*\*Python, SQL, Data Visualization, and Machine Learning\*\* to generate actionable operational insights and predict whether a flight is likely to be delayed.



\---



\## 🎯 Project Objectives



\- Analyze overall flight delay performance

\- Compare delay rates across airlines

\- Identify airports and routes with higher delay rates

\- Analyze delays by day and time of day

\- Understand major causes of flight delays

\- Build a Machine Learning model to predict flight delays

\- Create an interactive Streamlit dashboard

\- Generate business-oriented operational insights



\---



\## 📊 Dataset



The project uses historical U.S. flight reporting data.



Dataset size:



\- \*\*539,747 total flights\*\*

\- \*\*25 columns\*\*

\- \*\*16,312 cancelled flights\*\*

\- \*\*1,166 diverted flights\*\*

\- \*\*522,269 operated flights\*\*



The raw dataset is intentionally excluded from GitHub because of its large size.



\---



\## 🛠️ Technologies Used



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- Scikit-learn

\- SQLite

\- SQL

\- Streamlit

\- Git \& GitHub

\- Jupyter / VS Code



\---



\## 📁 Project Structure



```text

Flight\_Delay\_Analysis/

│

├── analysis/

│   ├── 01\_data\_inspection.py

│   ├── 02\_basic\_analysis.py

│   ├── 03\_airline\_analysis.py

│   ├── 04\_airport\_analysis.py

│   ├── 05\_route\_analysis.py

│   ├── 06\_time\_analysis.py

│   ├── 07\_day\_analysis.py

│   ├── 08\_delay\_cause\_analysis.py

│   ├── 09\_prepare\_prediction\_data.py

│   ├── 10\_feature\_engineering.py

│   ├── 11\_train\_test\_split.py

│   ├── 12\_encode\_features.py

│   ├── 13\_train\_model.py

│   ├── 14\_model\_evaluation.py

│   ├── 15\_improved\_model.py

│   ├── 16\_random\_forest\_model.py

│   ├── 17\_feature\_importance.py

│   ├── 18\_final\_model\_evaluation.py

│   ├── 19\_save\_final\_model.py

│   ├── 20\_business\_insights.py

│   ├── 21\_create\_visualizations.py

│   └── flight\_delay\_random\_forest.pkl

│

├── dashboard/

│   ├── app.py

│   └── README.md

│

├── images/

│   ├── 01\_overall\_delay\_rate.png

│   ├── 02\_airline\_delay\_rate.png

│   ├── 03\_airport\_delay\_rate.png

│   ├── 04\_route\_delay\_rate.png

│   ├── 05\_time\_of\_day\_delay\_rate.png

│   ├── 06\_day\_of\_week\_delay\_rate.png

│   ├── 07\_delay\_causes.png

│   └── 08\_arrival\_delay\_distribution.png

│

├── sql/

│   └── 01\_flight\_analysis.sql

│

├── .gitignore

└── README.md

