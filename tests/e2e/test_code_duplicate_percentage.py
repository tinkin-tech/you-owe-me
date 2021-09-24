from src.__main__ import generate_debt_report


def test_code_duplication_percentage():
    assert (
        generate_debt_report(
            "/home/dev-06/Desktop/tinkin/python/you-owe-me/tests/repository-fixture/"
        )
        == """
    Report Type      | Result
    -----------------|-----------
    Code Duplication | 40%
    """
    )
