# file paths
from pathlib import Path
from constants import DATA_DIR, CRYPTO_OUTPUT_DIR, RATINGS_OUTPUT_DIR
from config import round_number

# Ensure output directorys exist
Path(CRYPTO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(RATINGS_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Construct paths using pathlib's Path
mm_file = Path(DATA_DIR) / f'r{round_number}_crypto_v1_0_historical_meta_models.csv'
crypto_file = Path(CRYPTO_OUTPUT_DIR) / 'meta_model.csv'
ratings_file = Path(RATINGS_OUTPUT_DIR) / f'r{round_number}_ratings.csv'
