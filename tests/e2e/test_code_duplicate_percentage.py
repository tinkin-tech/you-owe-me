from src.__main__ import generate_debt_report
from os import path


def test_code_duplication_percentage():
    current_file_path = path.abspath(path.dirname(__file__))
    assert (
        generate_debt_report(path.join(current_file_path, "../demo-repository"))
        == """
    Report Type      | Result
    -----------------|-----------
    Code Duplication | 40%
    """
    )
