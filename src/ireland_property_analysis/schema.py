from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from ireland_property_analysis.exceptions import PropertyRawDataValidationError


@dataclass(frozen=True, kw_only=True)
class RawPropertyListing:
    """A property listing parsed from the source data."""

    date_of_sale: date
    county: str
    price: str
    description: str
    eircode: str = ""
    id: str = ""
    address: str = ""
    is_vat_exclusive: bool = False
    size_description: str = ""
    is_full_market_price: bool = True

    def __post_init__(self):
        if any(
            value is None
            for value in (self.date_of_sale, self.county, self.price, self.description)
        ):
            raise PropertyRawDataValidationError(
                "date_of_sale, county, price, and description must not be None"
            )
        if not isinstance(self.price, str) or not self.price.strip():
            raise PropertyRawDataValidationError("price must be a non-empty string")
        if "Ć" in self.price:
            object.__setattr__(self, "price", self.price.replace("Ć", "€"))


@dataclass(frozen=True, kw_only=True)
class CleanedPropertyListing:
    """A validated property listing with parsed price and area values."""

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
class ListingProcessingOutcome:
    """The cleaned listing or validation error for one source row."""

    row_number: str
    outcome: CleanedPropertyListing | PropertyRawDataValidationError


@dataclass(frozen=True)
class IngestionRunReport:
    """Counts and errors for one ingestion run."""

    total_records: int
    successful_records: int
    failed_records: int
    errors: dict[str, PropertyRawDataValidationError]