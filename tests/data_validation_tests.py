import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from exceptions import PropertyRawDataValidationError
from schema import RawPropertyListing


@pytest.fixture
def valid_property_data():
    return {
        "id": "prop-001",
        "date_of_sale": date(2010, 1, 4),
        "address": "49 ballynakelly green, newcastle",
        "county": "Dublin",
        "eircode": "D04 AB12",
        "price": 499600.00,
        "is_vat_exclusive": True,
        "description": "New Dwelling house /Apartment",
        "size_description": "greater than 125 sq metres",
        "is_full_market_price": False,
    }


def test_valid_property_data_is_accepted(valid_property_data):
    property_listing = RawPropertyListing(**valid_property_data)

    assert property_listing.date_of_sale == date(2010, 1, 4)
    assert property_listing.county == "Dublin"
    assert property_listing.price == 499600.00
    assert property_listing.is_full_market_price is False


def test_missing_date_of_sale_raises_validation_error(valid_property_data):
    invalid_data = valid_property_data.copy()
    invalid_data["date_of_sale"] = None

    with pytest.raises(PropertyRawDataValidationError, match="date_of_sale, county, price, and description must not be None"):
        RawPropertyListing(**invalid_data)


def test_missing_price_raises_validation_error(valid_property_data):
    invalid_data = valid_property_data.copy()
    invalid_data["price"] = None

    with pytest.raises(PropertyRawDataValidationError, match="date_of_sale, county, price, and description must not be None"):
        RawPropertyListing(**invalid_data)