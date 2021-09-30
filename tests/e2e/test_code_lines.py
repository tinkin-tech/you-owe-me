from src.__main__ import get_implementation_and_test_lines


def test_code_duplication_percentage():
    assert get_implementation_and_test_lines("tests/fixtures", "js,jsx") == {
        "IMPLEMENTATION_LINES": 3,
        "TEST_LINES": 40,
        "TOTAL_LINES": 43,
    }
