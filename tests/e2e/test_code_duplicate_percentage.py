from src.__main__ import generate_debt_report
from os import path


def test_code_duplication_percentage():
    assert (
        generate_debt_report("tests/demo-repository")
        == """
    Report Type      | Result
    -----------------|-----------
    Code Duplication | 40%
    """
    )
