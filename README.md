# Automated Machine Learning Pipeline for Dow Jones Industrial Average (DJI) Prediction

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/mohammadmostafavi-ai/AutoML-Asset-Pricing-Pipeline/blob/main/Thesis_Pipeline.ipynb)

## Abstract
This repository contains the source code for a specialized Automated Machine Learning (AutoML) pipeline developed to forecast the daily log-returns of the **Dow Jones Industrial Average (DJI)**.

Designed as part of a Master's Thesis in Theoretical Economics, this research framework integrates macroeconomic theory with computational intelligence. The pipeline aggregates data from over 50 historical constituents of the Dow Jones, major macroeconomic indicators, and qualitative geopolitical events to construct a high-dimensional feature space for empirical asset pricing models.

## Data Sources and Inputs
The model utilizes a heterogeneous dataset constructed from the following sources:
1.  **Target Variable:** Daily Log-Returns of the Dow Jones Industrial Average (`^DJI`).
2.  **Corporate Data:** Historical OHLCV (Open, High, Low, Close, Volume) data for 50+ historical and current constituents of the Dow Jones, sourced via Yahoo Finance with a "warm-up" period to ensure moving average consistency.
3.  **Macroeconomic Indicators:** Key economic drivers sourced from the Federal Reserve Economic Data (FRED), including Federal Funds Rate, CPI, GDP, and Unemployment Rate.
4.  **Global Market Indices:** Auxiliary financial variables including VIX, Gold, Oil (WTI), DXY, and major global indices (DAX, FTSE, Nikkei).
5.  **Qualitative Events:** A bespoke dataset of binary dummy variables representing major exogenous shocks, such as U.S. Presidential Elections, natural disasters, and significant political stability indices.

## Methodology
The pipeline follows a strict econometric and engineering workflow:

### 1. Preprocessing and Statistical Rigor
*   **Missing Value Imputation:** Hierarchical handling of missing data using out-of-index logic and forward-filling, strictly avoiding look-ahead bias.
*   **Outlier Management:** Application of **Winsorization** (0.5% - 99.5% quantiles) to variables with extreme kurtosis to mitigate the impact of distributional tails without data removal.
*   **Stationarity Tests:** Automated **Augmented Dickey-Fuller (ADF)** tests performed on all predictors to ensure time-series stability and prevent spurious regression results.
*   **Memory Optimization:** Aggressive downcasting of numerical datatypes (e.g., `float64` to `float32`) to enable high-dimensional processing in memory-constrained environments.

### 2. Feature Engineering
Technical indicators are generated for each constituent stock to capture momentum, volatility, and trend signals:
*   Moving Averages (SMA, EMA)
*   Relative Strength Index (RSI)
*   Moving Average Convergence Divergence (MACD)
*   Bollinger Bands and Average True Range (ATR)
*   Volume-weighted metrics (OBV, MFI)

### 3. Model Training and Selection
*   **Splitting Strategy:** A strict chronological split is used: Training (70%), Validation (15%), and Testing (15%).
*   **Baseline Model:** A Multivariate Linear Regression model is established as the econometric benchmark.
*   **AutoML Engine:** The **H2O.ai** framework is utilized to train and cross-validate a wide range of algorithms (GBM, DRF, GLM) within a 1-hour runtime limit (`max_runtime_secs=3600`), optimizing for Root Mean Squared Error (RMSE).

### 4. Evaluation and Interpretability
*   **Statistical Significance:** The **Diebold-Mariano Test** is implemented to statistically compare the predictive accuracy of the optimal H2O model against the linear baseline and other competing models.
*   **Explainable AI (XAI):** Post-hoc interpretation is conducted using **SHAP (SHapley Additive exPlanations)** values to quantify feature importance and non-linear relationships.

## Execution Environment
This script is specifically optimized for **Google Colab**. It includes an initialization module that automatically handles the installation of all dependencies (Java, H2O, technical analysis libraries).

**Usage:**
1.  Click the "Open in Colab" badge above (or open the `.ipynb` file).
2.  Execute the cells sequentially. The script is self-contained and requires no external configuration files.

## Outputs
The execution generates the following artifacts:
*   **Data Files:** `Thesis_Data_File.csv`, `Stationarity_Results.csv`, `Correlation_Results.csv`.
*   **Model Metrics:** `Baseline_Model_Performance.csv`, `H2O_AutoML_Leaderboard.csv`, `Diebold_Mariano_Test_Results.csv`.
*   **Visualizations:** `Scatter_Plot_Actual_vs_Predicted.png`, `Feature_Importance.png`, `SHAP_Summary_Plot.png`.

## Key Visualizations
### Prediction Accuracy (Actual vs Predicted)
![Scatter Plot](results/Scatter_Plot_Actual_vs_Predicted.png)

### Feature Importance
![Feature Importance](results/Feature_Importance.png)

### Model Explainability (SHAP)
![SHAP Summary](results/SHAP_Summary_Plot.png)

## License
Copyright (C) 2025 Mohammad Rasoul Mostafavi Marian

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License as published by the Free Software Foundation**, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [LICENSE](LICENSE) file for more details.

---
**Author:** Mohammad Rasoul Mostafavi Marian
*M.Sc. in Theoretical Economics | Researcher in Quantitative Finance*
