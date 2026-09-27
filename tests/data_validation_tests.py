from datetime import date
from decimal import Decimal

import pytest

from ireland_property_analysis.exceptions import PropertyRawDataValidationError
from ireland_property_analysis.schema import RawPropertyListing
from ireland_property_analysis.utils import (
    adjust_price_for_vat,
    parse_currency,
    parse_sqm,
)

# ROOT = get_root_dir()
# SRC = ROOT / "src"
# if str(SRC) not in sys.path:
#     sys.path.insert(0, str(SRC))


@pytest.fixture
def valid_property_data():
    return {
        "id": "prop-001",
        "date_of_sale": date(2010, 1, 4),
        "address": "49 ballynakelly green, newcastle",
        "county": "Dublin",
        "eircode": "D04 AB12",
        "price": "Ć365,110.13",
        "is_vat_exclusive": True,
        "description": "New Dwelling house /Apartment",
        "size_description": "greater than 125 sq metres",
        "is_full_market_price": False,
    }


def test_valid_property_data_is_accepted(valid_property_data):
    property_listing = RawPropertyListing(**valid_property_data)

    assert property_listing.date_of_sale == date(2010, 1, 4)
    assert property_listing.county == "Dublin"
    assert property_listing.price == "Ć365,110.13"
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
def test_empty_price_raises_validation_error(valid_property_data):
    invalid_data = valid_property_data.copy()
    invalid_data["price"] = ""

    with pytest.raises(PropertyRawDataValidationError, match="price must be a non-empty string"):
        RawPropertyListing(**invalid_data)


def test_parse_currency_removes_currency_formatting():
    assert parse_currency("EUR 365,110.13") == Decimal("365110.13")


def test_parse_currency_returns_zero_for_none():
    assert parse_currency(None) == Decimal("0")


@pytest.mark.parametrize(
    ("raw_area", "expected"),
    [
        ("greater than 125 sq metres", Decimal("125")),
        ("approximately 42.75 square metres", Decimal("42.75")),
    ],
)
def test_parse_sqm_extracts_area(raw_area, expected):
    assert parse_sqm(raw_area) == expected


@pytest.mark.parametrize("raw_area", ["", "no area specified"])
def test_parse_sqm_rejects_missing_or_invalid_area(raw_area):
    with pytest.raises(PropertyRawDataValidationError):
        parse_sqm(raw_area)


@pytest.mark.parametrize(
    ("vat_exclusive", "expected"),
    [(True, Decimal("113.5")), (False, Decimal("100"))],
)
def test_adjust_price_for_vat(vat_exclusive, expected):
    assert adjust_price_for_vat(Decimal("100"), vat_exclusive) == expected
