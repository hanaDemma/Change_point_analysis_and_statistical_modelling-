# Brent Oil Price Analysis

## Overview

This project analyzes historical Brent oil prices using statistical and machine learning models, including ARIMA, Bayesian inference, and LSTM. The goal is to detect change points, identify key economic and political factors influencing prices, and build predictive models for future trends.

Additionally, this project includes an interactive dashboard built with Flask (backend) and React (frontend) to visualize price trends and event correlations.


## Business Objective
The main objective of this project is to study how major global events impact Brent oil prices. This includes:

- Identifying key political, economic, and technological events that significantly affect oil prices.
- Measuring price fluctuations before and after key events (e.g., OPEC decisions, sanctions, conflicts).
- Providing data-driven insights for investors, policymakers, and energy companies.

## Folder Structure 

CHANGE_POINT_ANALYSIS_AND_STATISTICAL_MODELLING/
│── .github/

│── week10/

│── dashboard_screen_shot/

│── flask_backend/

│── notebooks/

│   │── change_point_analysis.ipynb

│   └── README.md

│ ── react-app/

│── scripts/

│   │── change_point_analysis.py

│   │── data_loader.py

│   │── plot.py

│── src/

│── tests/

│── .gitignore

│── README.md

└── requirements.txt

## Features

- 📈 Time Series Analysis – Extracts key insights from historical Brent oil price data.
- 🔍 Change Point Detection – Identifies significant trend shifts in the data using statistical methods.
- 🏛 Statistical Modeling – Implements models such as ARIMA and VAR for price forecasting.
- 🤖 Deep Learning Integration – Uses LSTM networks to capture complex price movement patterns.
- 📊 Data Visualization – Generates interactive plots using Matplotlib and Seaborn.
- ✅ Macroeconomic Factors – Study the effects of GDP, inflation, unemployment, and exchange rates on oil prices.
- 🔄 Automated Preprocessing – Handles missing values, feature extraction, and normalization.
- 📡 Model Evaluation – Calculates performance metrics like RMSE, MAE, and R² score for predictions.
- ✅ Interactive Dashboard – Visualize price trends using Flask (backend) and React (frontend).


## Technologies Used

The project uses Python, Flask, React, and various data science libraries:

* Backend (Flask)
   - Flask – API development
   - pandas & NumPy – Data processing
   - statsmodels – Statistical analysis
   - scikit-learn – Machine learning models
   - TensorFlow/Keras – Deep learning models
   - PyMC3 – Bayesian inference

* Frontend (React)
   - React.js – UI development
   - Recharts, D3.js – Interactive visualizations
   - react-chartjs-2 – Charts and graphs


## Installation

1️⃣ Clone the repository
To set up the project on your local machine, follow these steps:


1. Clone the repository:
   ```bash
   git clone https://github.com/hanaDemma/Change_point_analysis_and_statistical_modelling-
2. Navigate into the project directory:
   ```bash
   cd Change_point_analysis_and_statistical_modelling

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt


2️⃣ Set up the backend
   - cd flask_backend
   - pip install -r requirements.txt
   - flask run

3️⃣ Set up the frontend
   - cd ../react-app
   - npm install
   - npm run dev

4️⃣ Access the dashboard
Open http://localhost:5173 in your browser to view the React dashboard.

## Contributing

We welcome contributions to enhance the fraud detection system. Please follow these steps to contribute:

   - Fork the repository: Create a personal copy of the repository on GitHub.
   - Create a new branch: Develop your feature or fix in a separate branch.
   - Commit your changes: Ensure your commits are clear and descriptive.
   - Push to your fork: Upload your changes to your GitHub repository.
   - Create a Pull Request: Submit a PR to the main repository for review.
   License
   - For more information and detailed documentation, please refer to the README.md file.