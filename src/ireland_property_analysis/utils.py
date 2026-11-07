import re
from decimal import Decimal
from pathlib import Path

from ireland_property_analysis.exceptions import PropertyRawDataValidationError


def find_project_root() -> Path:
    """Find and return the project root directory."""
    start_dirs = (Path(__file__).resolve().parent, Path.cwd().resolve())
    for start_dir in start_dirs:
        for directory in (start_dir, *start_dir.parents):
            if (directory / "pyproject.toml").is_file():
                return directory

    searched_from = ", ".join(str(path) for path in start_dirs)
    raise FileNotFoundError(f"Could not find project root from {searched_from}")


def detect_file_encoding(path: str | Path) -> str:
    """Detect the encoding of a file."""
    from charset_normalizer import from_path

    match = from_path(path).best()
    return match.encoding if match else "utf-8"


def parse_currency(price_str: str | None) -> Decimal:
    """Parse a currency string into a Decimal amount."""
    if price_str is None:
        return Decimal(0)
    # Remove any characters that are not digits or decimal points
    cleaned_price = re.sub(r"[^0-9.]", "", price_str)
    return Decimal(cleaned_price)


def adjust_price_for_vat(price: Decimal, vat_exclusive: bool) -> Decimal:
    """Add VAT to an exclusive price; leave an inclusive price unchanged."""
    if vat_exclusive:
        return price * Decimal("1.135")  # Apply VAT (assuming 13.5% VAT rate)
    return price


def parse_area_sqm(raw_area: str) -> Decimal:
    """Read the first area value from a size description."""
    if not raw_area:
        raise PropertyRawDataValidationError("raw_area must not be None or empty")

    # Use regex to find the first occurrence of a number (integer or decimal)
    match = re.search(r"[0-9]+\.?[0-9]*", raw_area)
    if match:
        return Decimal(match.group())
    raise PropertyRawDataValidationError("No valid number found in raw_area")
