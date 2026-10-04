from unittest.mock import Mock

import pytest

from ireland_property_analysis import utils
from ireland_property_analysis.ingestion import stream_raw_records


def test_stream_raw_records_uses_detected_encoding_and_yields_csv_rows(
    tmp_path, monkeypatch
):
    csv_path = tmp_path / "properties.csv"
    csv_path.write_bytes(
        "id,address,price\n"
        '1,"12 Main Street, Dublin","€250,000"\n'
        '2,Café Road,"€310,500"\n'.encode("cp1252")
    )
    encoding_detector = Mock(return_value="cp1252")
    monkeypatch.setattr(utils, "get_file_encoding", encoding_detector)

    records = list(stream_raw_records(str(csv_path)))

    assert records == [
        {
            "id": "1",
            "address": "12 Main Street, Dublin",
            "price": "€250,000",
        },
        {"id": "2", "address": "Café Road", "price": "€310,500"},
    ]
    encoding_detector.assert_called_once_with(str(csv_path))


def test_stream_raw_records_returns_no_records_for_empty_file(tmp_path, monkeypatch):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")
    monkeypatch.setattr(utils, "get_file_encoding", Mock(return_value="utf-8"))

    assert list(stream_raw_records(str(csv_path))) == []


def test_stream_raw_records_propagates_missing_file_error(tmp_path, monkeypatch):
    missing_path = tmp_path / "missing.csv"
    monkeypatch.setattr(utils, "get_file_encoding", Mock(return_value="utf-8"))

    with pytest.raises(FileNotFoundError):
        list(stream_raw_records(str(missing_path)))
