class PropertyError(Exception):
    """Base class for property data errors."""
    note: str

    def __init__(self, note: str):
        self.note = note
        super().__init__(self.note)


class PropertyRawDataValidationError(PropertyError):
    """Raised when a property record fails validation."""
