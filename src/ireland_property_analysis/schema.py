from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from ireland_property_analysis.exceptions import PropertyRawDataValidationError


@dataclass(frozen=True, kw_only=True)
class RawPropertyListing:
    """
    Represents a raw property listing with basic information as from
    [the irish property register](https://www.propertyregister.ie)
    """

    date_of_sale: date
    county: str
    price: str
    description: str
    id: str = ""
    address: str = ""
    is_vat_exclusive: bool = False
    size_description: str = ""
    is_full_market_price: bool = True

    def __post_init__(self):
        if self.price.isspace() or not self.price:
            raise PropertyRawDataValidationError("price cannot be empty or whitespace")


@dataclass(frozen=True, kw_only=True)
class CleanedPropertyListing:
    """
    Represents a cleaned property listing with basic information as from
    [the irish property register](https://www.propertyregister.ie)
    """

    id: str
    date_of_sale: date
    county: str
    price: Decimal
    price_per_sq_m: Decimal
    description: str = ""
    address: str = ""
    is_vat_exclusive: bool = False
    size_description: str = ""
    is_full_market_price: bool = True

    def __post_init__(self):
        if self.price <= 0:
            raise PropertyRawDataValidationError("price must be greater than 0")
        if self.price_per_sq_m <= 0:
            raise PropertyRawDataValidationError(
                "price_per_sq_m must be greater than 0"
            )


@dataclass(frozen=True)
class RawRecordProcessOutcome:
    """
    Represents the outcome of processing raw records.
    Attributes:
        row_number (str): The row number of the processed record.
        outcome (CleanedPropertyListing | PropertyRawDataValidationError): The outcome of the processing operation.
    """

    row_number: str
    outcome: CleanedPropertyListing | PropertyRawDataValidationError

@dataclass(frozen=True)
class IngestionRunReport:
    """
    Represents the outcome of an ingestion run.
    Attributes:
        total_records (int): The total number of records processed.
        successful_records (int): The number of successfully processed records.
        failed_records (int): The number of failed records.
        errors (dict[str, PropertyRawDataValidationError]): A dictionary of errors encountered during processing.
    """

    total_records: int
    successful_records: int
    failed_records: int
    errors: dict[str, PropertyRawDataValidationError]