from datetime import datetime
from src.__main__ import generate_debt_report


def test_code_duplication_percentage():
    assert (
        generate_debt_report(
            "tests/demo-repository",
            datetime.strptime("2021-09-24", "%Y-%m-%d"),
            datetime.strptime("2021-09-27", "%Y-%m-%d"),
            int(1),
        )
        == """
        Report Type      | Date       |   Result  
        -----------------|------------|----------
     
        Code Duplication | 2021-09-25 | 40%
        -----------------|------------|-----------
    """
    )
