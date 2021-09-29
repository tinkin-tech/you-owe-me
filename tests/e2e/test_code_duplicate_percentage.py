from datetime import datetime
from src.__main__ import generate_debt_report


def test_code_duplication_percentage():
    assert (
        generate_debt_report(
            "tests/fixtures",
            datetime.strptime("2021-09-28", "%Y-%m-%d"),
            datetime.strptime("2021-09-30", "%Y-%m-%d"),
            1,
        )
        == """
        -------------|-------------------
        |   Date     | Code Duplication |  
        -------------|-------------------
        | 2021-09-28 |       40%        
        -------------|-------------------
        | 2021-09-29 |       33.33%        
        -------------|-------------------
        | 2021-09-30 |       33.33%        
        -------------|-------------------
    """
    )
