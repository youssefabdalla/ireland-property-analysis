class PropertyError(Exception):
    """Base class for exceptions in this module."""
    note: str

    def __init__(self, note: str):
        self.note = note
        super().__init__(self.note)


class PropertyRawDataValidationError(PropertyError):
    """Exception raised for errors in the raw property data."""
