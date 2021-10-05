from datetime import datetime
from src.__main__ import get_debt_report_by_range_date, format_debt_report


def test_debt_report():
    debt_report_by_range = get_debt_report_by_range_date(
        "tests/fixtures",
        datetime.strptime("2021-09-28", "%Y-%m-%d"),
        datetime.strptime("2021-09-30", "%Y-%m-%d"),
        1,
        "js,jsx",
    )
    assert (
        format_debt_report(debt_report_by_range)
        == "Date;Code Duplication;Implementation Lines;"
        "Test Lines; Total Lines\n"
        "2021-09-28;40%;0;19;19\n2021-09-29;33.33%;3;31;34\n"
        "2021-09-30;30.77%;3;40;43"
    )