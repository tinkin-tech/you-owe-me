from src.__main__ import get_implementation_and_test_lines


def test_code_implementation_lines():
    assert (
        get_implementation_and_test_lines(
            "tests/fixtures", "js,jsx", "implementation_lines"
        )
        == 79
    )


def test_code_test_lines():
    assert (
        get_implementation_and_test_lines(
            "tests/fixtures", "js,jsx", "test_lines"
        )
        == 14
    )


def test_code_total_lines():
    assert (
        get_implementation_and_test_lines(
            "tests/fixtures", "js,jsx", "total_lines"
        )
        == 93
    )
