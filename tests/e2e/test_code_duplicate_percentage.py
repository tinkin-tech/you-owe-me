import src.__main__
from src.__main__ import get_code_duplication_percentage


def test_code_duplication_percentage():
    src.__main__.DIRECTORY_PATH = "tests/fixtures"
    assert get_code_duplication_percentage() == "9.43%"
