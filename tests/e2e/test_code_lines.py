from src.__main__ import get_implementation_and_test_lines


def test_code_duplication_percentage():
    assert get_implementation_and_test_lines("tests/fixtures", "js,jsx") == {
        "IMPLEMENTATION_LINES": 14,
        "TEST_LINES": 79,
        "TOTAL_LINES": 93,
    }
