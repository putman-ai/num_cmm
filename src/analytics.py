# system imports
import logging
import warnings

from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore")

# third-party imports
import pandas as pd
import yfinance as yf

# configure logging
logging.basicConfig(level=logging.INFO)


def calculate_ratings(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """Calculate the rolling average ratings."""
    data['rating'] = data.groupby('symbol')['mm_rescaled'].rolling(window=window_size).mean().reset_index(level=0, drop=True)
    data['rating'] = data['rating'].round(2)
    data.dropna(inplace=True)
    logging.info(f"Calculated rolling average ratings with a window size of {window_size}")
    return data


def average_daily_ratings(data: pd.DataFrame) -> None:
    """Calculate and print the average rating for each day."""
    daily_average_ratings = data.groupby('date')['rating'].mean()
    daily_average_ratings = daily_average_ratings.round(2)


def save_data(data: pd.DataFrame, filepath: Path) -> None:
    """Save data to a CSV file."""
    data.to_csv(filepath, index=False)
    logging.info(f"Data saved to {filepath}")


def get_top_bottom_symbols(data: pd.DataFrame, date: pd.Timestamp) -> pd.DataFrame:
    """Get the top and bottom 10 symbols by rating."""
    daily_data = data[data['date'] == date][['date', 'symbol', 'rating']]
    sorted_data = daily_data.sort_values(by='rating', ascending=False)
    logging.info(f"Top and bottom symbols extracted for {date}")
    logging.info("Top 10 Tickers by rating:")
    logging.info(sorted_data['symbol'].head(10))
    logging.info("Bottom 10 Tickers by rating:")
    logging.info(sorted_data['symbol'].tail(10))
    return sorted_data