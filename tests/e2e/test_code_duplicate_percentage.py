from datetime import datetime
from src.__main__ import generate_debt_report


def test_code_duplication_percentage():
    assert (
        generate_debt_report(
            "tests/you-owe-me-test",
            datetime.strptime("2021-09-24", "%Y-%m-%d"),
            datetime.strptime("2021-09-27", "%Y-%m-%d"),
            1,
        )
        == """
        -------------|-------------------
        |   Date     | Code Duplication |  
        -------------|-------------------
        | 2021-09-24 |       40%        |
        -------------|-------------------
        | 2021-09-25 |       40%        |
        -------------|-------------------
        | 2021-09-26 |       40%        |
        -------------|-------------------
        | 2021-09-27 |       40%        |
        -------------|-------------------
    """
    )
