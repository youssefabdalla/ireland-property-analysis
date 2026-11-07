from unittest.mock import Mock

import pytest

from ireland_property_analysis import ingestion
from ireland_property_analysis.exceptions import PropertyRawDataValidationError


def test_iter_raw_csv_rows_uses_detected_encoding_and_yields_rows(
    tmp_path, monkeypatch
):
    csv_path = tmp_path / "properties.csv"
    csv_path.write_bytes(
        "address,price\n"
        '"12 Main Street, Dublin","€250,000"\n'
        'Café Road,"€310,500"\n'.encode("cp1252")
    )
    encoding_detector = Mock(return_value="cp1252")
    monkeypatch.setattr(ingestion, "detect_file_encoding", encoding_detector)

    records = list(ingestion.iter_raw_csv_rows(csv_path))

    assert records == [
        {
            "id": "2",
            "address": "12 Main Street, Dublin",
            "price": "€250,000",
        },
        {"id": "3", "address": "Café Road", "price": "€310,500"},
    ]
    encoding_detector.assert_called_once_with(csv_path)


def test_iter_raw_csv_rows_returns_no_rows_for_empty_file(tmp_path, monkeypatch):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")
    monkeypatch.setattr(
        ingestion, "detect_file_encoding", Mock(return_value="utf-8")
    )

    assert list(ingestion.iter_raw_csv_rows(csv_path)) == []


def test_iter_raw_csv_rows_propagates_missing_file_error(tmp_path, monkeypatch):
    missing_path = tmp_path / "missing.csv"
    monkeypatch.setattr(
        ingestion, "detect_file_encoding", Mock(return_value="utf-8")
    )

    with pytest.raises(FileNotFoundError):
        list(ingestion.iter_raw_csv_rows(missing_path))


def test_parse_raw_property_listing_defaults_nullable_optional_values():
    listing = ingestion.parse_raw_property_listing(
        {
            "Date of Sale (dd/mm/yyyy)": "01/01/2010",
            "County": "Dublin",
            "Price (Ć)": "€250,000",
            "Address": None,
            "Description of Property": None,
            "VAT Exclusive": None,
            "Property Size Description": None,
            "Not Full Market Price": None,
        }
    )

    assert listing.address == ""
    assert listing.description == ""
    assert listing.is_vat_exclusive is False
    assert listing.size_description == ""
    assert listing.is_full_market_price is True


@pytest.mark.parametrize(
    "field_name",
    ["Date of Sale (dd/mm/yyyy)", "County", "Price (Ć)"],
)
def test_parse_raw_property_listing_rejects_null_required_values(field_name):
    row: dict[str, str | None] = {
        "Date of Sale (dd/mm/yyyy)": "01/01/2010",
        "County": "Dublin",
        "Price (Ć)": "€250,000",
    }
    row[field_name] = None

    with pytest.raises(
        PropertyRawDataValidationError, match="Missing required CSV value"
    ):
        ingestion.parse_raw_property_listing(row)
