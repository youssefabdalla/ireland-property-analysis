import csv
from collections.abc import Iterator
from pathlib import Path

from dateutil import parser as date_parser

from ireland_property_analysis.schema import (
    CleanedPropertyListing,
    IngestionRunReport,
    RawPropertyListing,
    RawRecordProcessOutcome,
)

from .utils import *


def stream_raw_records(file_path: str) -> Iterator[dict[str, str | None]]:
    """
    Stream raw records from a CSV file.
    Args:
        file_path (str): The path to the CSV file.
    Yields:
        dict: A dictionary representing a single record from the CSV file.
    """
    # Ensure the file encoding is determined
    encoding = get_file_encoding(file_path)
    with open(Path(file_path), "r", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row_number, row in enumerate(reader, start=2):
            row["id"] = str(row_number)
            yield row


def process_raw_record(raw_record: dict) -> RawPropertyListing:
    """
    Process a raw record and convert it into a RawPropertyListing.
    Args:
        raw_record (dict): A dictionary representing a single raw record.
    Returns:
        RawPropertyListing: An instance of RawPropertyListing containing the processed data.
    """
    try:
        id = raw_record.get("id", "")
        date_of_sale = date_parser.parse(raw_record["Date of Sale (dd/mm/yyyy)"]).date()
        county = raw_record["County"]
        price = raw_record["Price (Ć)"]
        description = raw_record.get("Description of Property", "")
        address = raw_record.get("Address", "")
        is_vat_exclusive = raw_record.get("VAT Exclusive", "No") == "Yes"
        size_description = raw_record.get("Property Size Description", "")
        is_full_market_price = raw_record.get("Not Full Market Price", "No") == "No"

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


def process_raw_property_listing(
    raw_listing: RawPropertyListing,
) -> RawRecordProcessOutcome:
    """
    Process a RawPropertyListing and convert it into a CleanedPropertyListing.
    Args:
        raw_listing (RawPropertyListing): An instance of RawPropertyListing to process.
    Returns:
        RawRecordProcessOutcome: The outcome of the processing operation.
    """
    try:
        price = parse_currency(raw_listing.price)
        price = adjust_price_for_vat(price, raw_listing.is_vat_exclusive)
        area_sqm = parse_sqm(raw_listing.size_description)
        price_per_sq_m = price / area_sqm
        return RawRecordProcessOutcome(
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
        return RawRecordProcessOutcome(
            row_number=raw_listing.id,
            outcome=PropertyRawDataValidationError(
                f"Error processing record at row {raw_listing.id}: {e}"
            ),
        )


def report_ingestion_run(
    processed_records: list[RawRecordProcessOutcome],
) -> IngestionRunReport:
    """
    Generate a report summarizing the results of an ingestion run.
    Args:
        processed_records (list[RawRecordProcessOutcome]): A list of RawRecordProcessOutcome instances.
    Returns:
        IngestionRunReport: A report summarizing the ingestion run.
    """
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
