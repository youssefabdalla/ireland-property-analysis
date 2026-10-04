from pathlib import Path


def stream_raw_records(file_path: str):
    """
    Stream raw records from a CSV file.
    Args:
        file_path (str): The path to the CSV file.
    Yields:
        dict: A dictionary representing a single record from the CSV file.
    """
    import csv

    from .utils import get_file_encoding
    # Ensure the file encoding is determined
    encoding = get_file_encoding(file_path)
    with open(Path(file_path), "r", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        yield from reader
