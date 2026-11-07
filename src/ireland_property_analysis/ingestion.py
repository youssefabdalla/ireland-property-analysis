import csv
from collections.abc import Iterator
from pathlib import Path

from dateutil import parser as date_parser

from ireland_property_analysis.exceptions import PropertyRawDataValidationError
from ireland_property_analysis.schema import (
    CleanedPropertyListing,
    IngestionRunReport,
    ListingProcessingOutcome,
    RawPropertyListing,
)

from .utils import (
    adjust_price_for_vat,
    detect_file_encoding,
    parse_area_sqm,
    parse_currency,
)


def iter_raw_csv_rows(file_path: str | Path) -> Iterator[dict[str, str | None]]:
    """Yield CSV rows as dictionaries and add each row's file line number."""
    encoding = detect_file_encoding(file_path)
    with open(file_path, "r", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row_number, row in enumerate(reader, start=2):
            row["id"] = str(row_number)
            yield row


def _required_csv_value(
    raw_record: dict[str, str | None], field_name: str
) -> str:
    value = raw_record.get(field_name)
    if value is None:
        raise PropertyRawDataValidationError(
            f"Missing required CSV value for {field_name}"
        )
    return value


def _optional_csv_value(
    raw_record: dict[str, str | None], field_name: str, default: str = ""
) -> str:
    value = raw_record.get(field_name)
    return default if value is None else value


def parse_raw_property_listing(
    raw_record: dict[str, str | None],
) -> RawPropertyListing:
    """Convert a CSV row into a validated raw property listing."""
    try:
        id = _optional_csv_value(raw_record, "id")
        date_of_sale = date_parser.parse(
            _required_csv_value(raw_record, "Date of Sale (dd/mm/yyyy)")
        ).date()
        county = _required_csv_value(raw_record, "County")
        price = _required_csv_value(raw_record, "Price (Ć)")
        description = _optional_csv_value(raw_record, "Description of Property")
        address = _optional_csv_value(raw_record, "Address")
        is_vat_exclusive = (
            _optional_csv_value(raw_record, "VAT Exclusive", "No") == "Yes"
        )
        size_description = _optional_csv_value(
            raw_record, "Property Size Description"
        )
        is_full_market_price = (
            _optional_csv_value(raw_record, "Not Full Market Price", "No") == "No"
        )

        return RawPropertyListing(
            date_of_sale=date_of_sale,
            county=county,
            price=price,
            description=description,
            id=id,
            address=address,
            is_vat_exclusive=is_vat_exclusive,
            size_description=size_description,
            is_full_market_price=is_full_market_price,
        )
    except (ValueError, TypeError, ArithmeticError, KeyError) as e:
        raise PropertyRawDataValidationError(
            f"Error processing record: with id {raw_record.get('id', 'Unknown')}: {e}"
        ) from e


def clean_listing_with_outcome(
    raw_listing: RawPropertyListing,
) -> ListingProcessingOutcome:
    """Clean a listing and return either the cleaned listing or its validation error."""
    try:
        price = parse_currency(raw_listing.price)
        price = adjust_price_for_vat(price, raw_listing.is_vat_exclusive)
        area_sqm = parse_area_sqm(raw_listing.size_description)
        price_per_sq_m = price / area_sqm
        return ListingProcessingOutcome(
            row_number=raw_listing.id,
            outcome=CleanedPropertyListing(
                id=raw_listing.id,
                date_of_sale=raw_listing.date_of_sale,
                county=raw_listing.county,
                price=price,
                price_per_sq_m=price_per_sq_m,
                description=raw_listing.description,
                address=raw_listing.address,
                is_vat_exclusive=raw_listing.is_vat_exclusive,
                size_description=raw_listing.size_description,
                is_full_market_price=raw_listing.is_full_market_price,
            ),
        )
    except (
        PropertyRawDataValidationError,
        ValueError,
        TypeError,
        ArithmeticError,
    ) as e:
        return ListingProcessingOutcome(
            row_number=raw_listing.id,
            outcome=PropertyRawDataValidationError(
                f"Error processing record at row {raw_listing.id}: {e}"
            ),
        )


def summarize_ingestion_run(
    processed_records: list[ListingProcessingOutcome],
) -> IngestionRunReport:
    """Count successful and failed listings in an ingestion run."""
    total_records = len(processed_records)
    successful_records = sum(
        1
        for record in processed_records
        if isinstance(record.outcome, CleanedPropertyListing)
    )
    failed_records = total_records - successful_records
    errors = {
        record.row_number: record.outcome
        for record in processed_records
        if isinstance(record.outcome, PropertyRawDataValidationError)
    }

    return IngestionRunReport(
        total_records=total_records,
        successful_records=successful_records,
        failed_records=failed_records,
        errors=errors,
    )
