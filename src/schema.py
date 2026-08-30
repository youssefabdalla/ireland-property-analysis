from dataclasses import dataclass
from datetime import date

from exceptions import PropertyRawDataValidationError


@dataclass(frozen=True, init=False)
class RawPropertyListing:
    """
    Represents a raw property listing with basic information as from
    [the irish property register](https://www.propertyregister.ie)
    """
    id: str = ""
    date_of_sale: date | None = None
    address: str = ""
    county: str = ""
    eircode: str = ""
    price: float | None = None
    is_vat_exclusive: bool = False
    description: str = ""
    size_description: str = ""
    is_full_market_price: bool = True

    def __init__(
        self,
        date_of_sale: date,
        county: str,
        price: float,
        description: str,
        *,
        id: str = "",
        address: str = "",
        eircode: str = "",
        is_vat_exclusive: bool = False,
        size_description: str = "",
        is_full_market_price: bool = True,
    ):
        if (date_of_sale is None) or (county is None) or (price is None) or (description is None):
            raise PropertyRawDataValidationError(
                "date_of_sale, county, price, and description must not be None")

        object.__setattr__(self, "id", id)
        object.__setattr__(self, "date_of_sale", date_of_sale)
        object.__setattr__(self, "address", address)
        object.__setattr__(self, "county", county)
        object.__setattr__(self, "eircode", eircode)
        object.__setattr__(self, "price", price)
        object.__setattr__(self, "is_vat_exclusive", is_vat_exclusive)
        object.__setattr__(self, "description", description)
        object.__setattr__(self, "size_description", size_description)
        object.__setattr__(self, "is_full_market_price", is_full_market_price)
