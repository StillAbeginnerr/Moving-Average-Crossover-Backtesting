# Moving Average Crossover Backtesting

This repository contains a Python script that demonstrates a simple backtesting framework for a **moving average crossover strategy** on historical stock price data. The strategy is based on the concept of price action and uses two simple moving averages (SMAs):

- **Buy Signal**: When the short-term SMA (20-day) crosses above the long-term SMA (50-day).
- **Sell Signal**: When the short-term SMA crosses below the long-term SMA.

## Features

- **Data Loading & Cleaning**:  
  The script loads historical price data from a CSV file, skipping extra header rows and parsing dates correctly.  
- **Technical Indicators**:  
  It computes the 20-day and 50-day SMAs.
- **Signal Generation**:  
  Buy and sell signals are generated based on the SMA crossover.
- **Return Calculation**:  
  The script calculates daily returns and cumulative returns for both the market and the strategy.
- **Visualization**:  
  It plots the closing price, SMAs, and marks buy/sell signals on a chart.
- **Performance Metrics**:  
  Cumulative market and strategy returns are printed to evaluate the strategy's performance.



