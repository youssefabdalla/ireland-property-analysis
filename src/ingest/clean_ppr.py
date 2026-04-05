import pandas as pd
from pathlib import Path
import re
PROCESSED_DATA_DIR = Path("data/processed")
def clean_ppr_data(input_csv: Path, output_csv: Path):
    """Cleans the raw PPR data and saves the cleaned version."""
    # 0. Ensure output folder exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # 1. Load the raw CSV
    df = pd.read_csv(input_csv, encoding='cp1252')
    
    # 2. Basic cleaning steps
    df.columns = (
    df.columns
    .str.replace(r'[^\w\s]', '', regex=True) # Removes (€) and other symbols
    .str.strip()                             # Removes leading/trailing spaces
    .str.replace(' ', '_')                   # Replaces middle spaces with underscores
    .str.lower()                             # Makes everything lowercase
)
    
    # 3. Convert data types (e.g., price to numeric, date to datetime)
    df['price_clean'] = df['price'].apply(__clean_currency)
    
    # 4. create boolean column for vat exclusive
    df['is_vat_exclusive'] = df['vat_exclusive'].str.contains('Yes',case=False, na=False)
    
    # 5. Save the cleaned data to a new CSV
    df.to_csv(output_csv, index=False)


def __clean_currency(price_str):
    if pd.isna(price_str):
        return None
    # remove everything that isn't a digit or descimal point
    clean_str = re.sub(r'[^\d.]','',str(price_str))
    # convert clean_str to floot which handles the .00 then to int
    try:
        return int(float(clean_str))
    except ValueError:
        return None