import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, "./")
from src.utils.utils_date import validate_date_range, format_date

load_dotenv()


def load_environment_variables():
    check_for_environment_variables(
        ["START_DATE", "END_DATE", "INTERVAL_IN_DAYS"]
    )

    start_date = format_date(os.getenv("START_DATE"))
    end_date = format_date(os.getenv("END_DATE"))
    validate_date_range(start_date, end_date)

    return {
        "START_DATE": start_date,
        "END_DATE": end_date,
        "INTERVAL_IN_DAYS": int(os.getenv("INTERVAL_IN_DAYS")),
    }


def check_for_environment_variables(variables):
    for variable in variables:
        if os.getenv(variable) is None:
            raise ValueError(f"Variable {variable} is not defined")
