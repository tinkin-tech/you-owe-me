import src.__main__
from src.__main__ import get_implementation_and_test_lines


def test_code_duplication_percentage():
    src.__main__.DIRECTORY_PATH = "tests/fixtures"
    src.__main__.FILE_EXTENSIONS = "js,jsx"
    assert get_implementation_and_test_lines() == {
        "IMPLEMENTATION_LINES": 14,
        "TEST_LINES": 79,
        "TOTAL_LINES": 93,
    }
