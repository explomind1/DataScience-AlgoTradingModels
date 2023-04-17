import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def detect_fibo_retracement(df, threshold=0.05):
    '''
    Detects Fibonacci retracement moments in a time series data.

    Parameters:
    df (pd.DataFrame): The time series data. Must have columns named 'high' and 'low'.
    threshold (float): The threshold for the difference between the actual and expected retracement levels.

    Returns:
    retracements (pd.DataFrame): A dataframe with the retracement levels and the associated dates.
    '''
    # Compute the range of the data
    data_range = df['high'].max() - df['low'].min()

    # Define the Fibonacci levels to be detected
    fibo_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

    # Compute the expected retracement levels
    retracement_levels = [df['high'].max() - fibo_level * data_range for fibo_level in fibo_levels]

    # Find the actual retracement levels
    retracement_values = [df['low'].min() + (df['high'].max() - df['low'].min()) * fibo_level for fibo_level in fibo_levels]

    # Find the indices of the closest actual retracement values to the expected ones
    indices = [np.argmin(np.abs(df['low'] - retracement_value)) for retracement_value in retracement_values]

    # Compute the difference between the actual and expected retracement levels
    differences = [np.abs(df.iloc[index]['low'] - expected_level) for index, expected_level in zip(indices, retracement_levels)]

    # Detect the retracement moments
    retracement_moments = df.iloc[np.where(np.array(differences) < threshold)[0]]

    # Create a dataframe with the retracement levels and the associated dates
    retracements = pd.DataFrame({'Level': fibo_levels, 'Value': retracement_values, 'Date': df.index[indices]})

    # Return the retracements dataframe
    return retracements

def visualize_fibo_retracement(df, retracements):
    '''
    Visualizes the time series data and the Fibonacci retracement levels.

    Parameters:
    df (pd.DataFrame): The time series data. Must have columns named 'high' and 'low'.
    retracements (pd.DataFrame): The dataframe with the retracement levels and the associated dates.
    '''
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

    # Plot the time series data on the first subplot
    ax1.plot(df.index, df['close'])
    ax1.set_ylabel('Price')
    ax1.set_title('Time series data with Fibonacci retracement levels')

    # Plot the Fibonacci retracement levels on the second subplot
    ax2.plot(df.index, df['close'])
    for level, value, date in zip(retracements['Level'], retracements['Value'], retracements['Date']):
        ax2.axhline(y=value, color='r', linestyle='--')
        ax2.text(df.index[-1], value, f'Level {level}: {value:.2f}', ha='right', va='center')
        ax2.axvline(x=date, color='r', linestyle='
