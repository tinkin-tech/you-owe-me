from datetime import datetime
from src.__main__ import get_debt_report_by_range_date, format_debt_report


def test_debt_report():
    debt_report_by_range = get_debt_report_by_range_date(
        "tests/fixtures",
        "js,jsx",
        datetime.strptime("2021-10-01", "%Y-%m-%d"),
        datetime.strptime("2021-10-21", "%Y-%m-%d"),
        7,
    )
    assert (
        format_debt_report(debt_report_by_range)
        == "Date;Code Duplication;Implementation Lines;"
        "Test Lines;Total Lines;Coverage\n"
        "2021-10-07;9.43%;79;14;93;66.66%\n"
        "2021-10-14;9.43%;79;14;93;66.66%\n"
        "2021-10-21;8.33%;88;14;102;62%"
    )
