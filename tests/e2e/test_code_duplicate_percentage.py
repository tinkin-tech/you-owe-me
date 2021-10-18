from src.__main__ import get_code_duplication_percentage


def test_code_duplication_percentage():
    assert get_code_duplication_percentage("tests/fixtures") == "8.33%"
