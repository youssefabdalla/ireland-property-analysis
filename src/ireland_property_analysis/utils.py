import re
from decimal import Decimal
from pathlib import Path

from ireland_property_analysis.exceptions import PropertyRawDataValidationError


def get_root_dir() -> Path:
    """
    Get the root directory of the project by searching for a 'pyproject.toml' file.
    Returns:
        Path: The root directory of the project.
    """
    start_dirs = (Path(__file__).resolve().parent, Path.cwd().resolve())
    for start_dir in start_dirs:
        for directory in (start_dir, *start_dir.parents):
            if (directory / "pyproject.toml").is_file():
                return directory

    searched_from = ", ".join(str(path) for path in start_dirs)
    raise FileNotFoundError(
        f"Could not find project root from {searched_from}")


def get_file_encoding(path: str) -> str:
    """
    Get the file encoding used in the project.
    Returns:
        str: The file encoding used in the project.
    """
    from charset_normalizer import from_path

    match = from_path(path).best()
    return match.encoding


def parse_currency(price_str: str | None) -> Decimal:
    """
    Parse a currency string and return its decimal value.
    Args:
        price_str (str): The currency string to parse.
    Returns:
        decimal.Decimal: The parsed currency value.
    """
    if price_str is None:
        return Decimal(0)
    # Remove any characters that are not digits or decimal points
    cleaned_price = re.sub(r"[^0-9.]", "", price_str)
    return Decimal(cleaned_price)


def adjust_price_for_vat(price: Decimal, vat_exclusive: bool) -> Decimal:
    """
    Adjust the price based on whether it is VAT exclusive or inclusive.
    Args:
        price (decimal.Decimal): The original price.
        vat_exclusive (bool): Whether the price is VAT exclusive.
    Returns:
        decimal.Decimal: The adjusted price.
    """
    if vat_exclusive:
        return price * Decimal('1.135')  # Apply VAT (assuming 13.5% VAT rate)
    return price


def parse_sqm(raw_area: str) -> Decimal:
    """
    Parse a raw area string and return its decimal value in square meters.
    Args:
        raw_area (str): The raw area string to parse.
    Returns:
        decimal.Decimal: The parsed area value in square meters.
    Raises:
        PropertyRawDataValidationError: If the raw_area is None, empty, or does not contain a valid number.
    """
    if not raw_area:
        raise PropertyRawDataValidationError(
            "raw_area must not be None or empty")

    # Use regex to find the first occurrence of a number (integer or decimal)
    match = re.search(r"[0-9]+\.?[0-9]*", raw_area)
    if match:
        return Decimal(match.group())
    raise PropertyRawDataValidationError("No valid number found in raw_area")
