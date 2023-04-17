import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_cup_and_handle(data, depth_ratio_threshold=0.5, handle_ratio_threshold=0.5):
    formations = []

    for i in range(len(data) - 5):
        left_peak = data.iloc[i]
        cup_bottom = data.iloc[i + 2]
        right_peak = data.iloc[i + 4]

        if left_peak['High'] < right_peak['High']:
            continue

        depth_ratio = (left_peak['High'] - cup_bottom['Low']) / left_peak['High']
        if depth_ratio < depth_ratio_threshold:
            continue

        handle_ratio = (right_peak['High'] - cup_bottom['Low']) / (left_peak['High'] - cup_bottom['Low'])
        if handle_ratio > handle_ratio_threshold:
            continue

        formations.append((i, i + 4))

    return formations

def plot_cup_and_handle(data, formations):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price')

    for formation in formations:
        left_peak = data.iloc[formation[0]]
        cup_bottom = data.iloc[formation[0] + 2]
        right_peak = data.iloc[formation[1]]

        plt.plot([left_peak.name, cup_bottom.name, right_peak.name],
                 [left_peak['High'], cup_bottom['Low'], right_peak['High']],
                 'r-o', label='Cup and Handle')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Cup and Handle Formations')
    plt.show()

# Read your Forex data
# data = pd.read_csv('your_forex_data.csv', index_col='Date', parse_dates=True)

# For the sake of this example, we will generate some random data
data = pd.DataFrame(np.random.randn(100, 4), columns=['Open', 'High', 'Low', 'Close'])
data.index = pd.date_range('2023-01-01', periods=len(data), freq='D')

formations = find_cup_and_handle(data)
plot_cup_and_handle(data, formations)
