# pipeline.py 

# system imports
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# third-party libraries
import pandas as pd

# local libraries
import analytics as an
import data_processing as dp
import visualizations as vis

from pathlib import Path
from paths import mm_file, crypto_file, ratings_file
from config import round_number, window_size

# Load and process data
mm_data = dp.load_data(mm_file)
mm_data = dp.filter_recent_tokens(mm_data)

# Rescale the 'meta_model' and drop the original column
mm_data['mm_rescaled'] = mm_data['meta_model'] * 5
mm_data.drop('meta_model', axis=1, inplace=True)
    
# Reindex and fill missing data
complete_mm_data = dp.reindex_and_fill(mm_data)

# Calculate rolling ratings
complete_mm_data = an.calculate_ratings(complete_mm_data, window_size)

# Save processed data
an.save_data(complete_mm_data, crypto_file)

# top and bottom symbols
today = pd.Timestamp.today().normalize()
top_bottom = an.get_top_bottom_symbols(complete_mm_data, today)

# Save and display top/bottom tickers
an.save_data(top_bottom, ratings_file)

