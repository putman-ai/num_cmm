# data processing
import pandas as pd

from pathlib import Path

def load_data(filepath: Path) -> pd.DataFrame:
    """Load and preprocess the meta model data."""
    try:
        data = pd.read_csv(filepath)
        data['date'] = pd.to_datetime(data['date'])
        # logging.info(f"Data loaded successfully from {filepath}")
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        raise

def filter_recent_tokens(data: pd.DataFrame) -> pd.DataFrame:
    """Filter the tokens to keep only those present on the most recent date."""
    most_recent_date = data['date'].max()
    recent_tokens = data[data['date'] == most_recent_date]['symbol'].unique()
    # logging.info(f"Filtered recent tokens for the date {most_recent_date}")
    return data[data['symbol'].isin(recent_tokens)]

def reindex_and_fill(data):
    """Reindex the data to include all dates and fill missing values."""
    full_date_range = pd.date_range(start=data['date'].min(), end=pd.Timestamp.today(), freq='D')
    symbol_data_frames = []
    
    for symbol, group in data.groupby('symbol'):
        group = group.set_index('date').reindex(full_date_range)
        group['symbol'] = symbol
        group['mm_rescaled'] = group['mm_rescaled'].ffill()
        symbol_data_frames.append(group)
    
    complete_data = pd.concat(symbol_data_frames).reset_index()
    complete_data = complete_data.rename(columns={'index': 'date'})
    complete_data = complete_data.dropna()
    
    return complete_data