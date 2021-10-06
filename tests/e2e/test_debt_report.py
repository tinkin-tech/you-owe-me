from datetime import datetime
import src.__main__
from src.__main__ import get_debt_report_by_range_date, format_debt_report


def test_debt_report():
    src.__main__.DIRECTORY_PATH = "tests/fixtures"
    src.__main__.FILE_EXTENSIONS = "js,jsx"
    debt_report_by_range = get_debt_report_by_range_date(
        datetime.strptime("2021-09-28", "%Y-%m-%d"),
        datetime.strptime("2021-09-30", "%Y-%m-%d"),
        1,
    )
    assert (
        format_debt_report(debt_report_by_range)
        == "Date;Code Duplication;Implementation Lines;"
        "Test Lines; Total Lines\n"
        "2021-09-28;40%;0;19;19\n"
        "2021-09-29;30.77%;3;40;43\n"
        "2021-09-30;30.77%;3;40;43"
    )
