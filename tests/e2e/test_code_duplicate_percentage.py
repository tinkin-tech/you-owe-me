from src.__main__ import get_percentage_code_duplication


def test_code_duplication_percentage():
    assert get_percentage_code_duplication("tests/fixtures") == "9.43%"
