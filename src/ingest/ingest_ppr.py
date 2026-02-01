import requests
import zipfile
import io
from pathlib import Path
import certifi
import logging
# setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Constants
PPR_ZIP_URL = "https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip"
RAW_DATA_DIR = Path("data/raw")

def download_and_extract_ppr():
    """Downloads the full Ireland Property Price Register and extracts the CSV."""
    # 1. Ensure folder exists
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading data from {PPR_ZIP_URL}")
    try:
        # 2. Download zip file
        response = requests.get(PPR_ZIP_URL, timeout=30,verify=certifi.where())
        response.raise_for_status()
    except requests.exceptions.SSLError:
        # Try 2: The Fallback (Necessary for this specific Gov site in Codespaces)
        logger.warning("SSL Verification failed. Falling back to unverified download...")
        response = requests.get(PPR_ZIP_URL, timeout=60, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to Download raw PPR data: {e}")
        # 3. unzip in memory for efficiency
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # one file in this zip PPR-ALL.zip
            file_name = z.namelist()[0]
            logger.info(f"extracting {file_name}...")
            # 4. save to raw data folder
            z.extractall(path=RAW_DATA_DIR)
            logger.info(f"success! PPR raw data saved to {RAW_DATA_DIR/file_name}")
    except zipfile.BadZipFile as e:
        logger.error(f"Bad zip file from {PPR_ZIP_URL}: {e}")