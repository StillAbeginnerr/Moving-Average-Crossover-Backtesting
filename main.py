import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and Clean the Data
# Skip the first three rows and manually assign column names.
df = pd.read_csv(
    'AAPL_data.csv', 
    skiprows=3, 
    names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'], 
    parse_dates=['Date'],
    index_col='Date'
)

# Ensure the data is sorted by date
df.sort_index(inplace=True)

# 2. Calculate Moving Averages for the Strategy
short_window = 20  # e.g., 20-day SMA
long_window = 50   # e.g., 50-day SMA

df['SMA_20'] = df['Close'].rolling(window=short_window).mean()
df['SMA_50'] = df['Close'].rolling(window=long_window).mean()

# 3. Define the Trading Signals
# When the 20-day SMA is above the 50-day SMA, signal = 1 (buy); otherwise, -1 (sell).
df['Signal'] = 0
df.loc[df['SMA_20'] > df['SMA_50'], 'Signal'] = 1
df.loc[df['SMA_20'] <= df['SMA_50'], 'Signal'] = -1

# 4. Calculate Returns
# Calculate the daily return of the asset.
df['Daily_Return'] = df['Close'].pct_change()

# Calculate strategy return by using the signal from the previous day (to avoid lookahead bias).
df['Strategy_Return'] = df['Signal'].shift(1) * df['Daily_Return']

# Compute cumulative returns for both the market and the strategy.
df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

# 5. Plot the Results
plt.figure(figsize=(14, 7))

# Plot closing prices and moving averages.
plt.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.5)
plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='green', alpha=0.7)
plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='red', alpha=0.7)

# Plot buy signals (green up arrows) and sell signals (red down arrows).
buy_signals = df[df['Signal'] == 1]
sell_signals = df[df['Signal'] == -1]
plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)

plt.title('Moving Average Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid()
plt.show()

# 6. Print Final Performance Metrics
final_market_return = df['Cumulative_Market_Return'].iloc[-1] - 1
final_strategy_return = df['Cumulative_Strategy_Return'].iloc[-1] - 1

print("Cumulative Market Return: {:.2f}%".format(final_market_return * 100))
print("Cumulative Strategy Return: {:.2f}%".format(final_strategy_return * 100))
