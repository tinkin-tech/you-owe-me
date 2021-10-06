import os
from dotenv import load_dotenv
from src.utils.date import (
    validate_date_range,
    parse_date_string_to_datetime,
)

load_dotenv()

ENVIRONMENT_VARIABLE_NAMES = [
    "START_DATE",
    "END_DATE",
    "INTERVAL_IN_DAYS",
    "FILE_EXTENSIONS",
    "PATTERN_TEST_FILES",
    "PATTERN_IMPLEMENTATION_FILES",
]


def load_environment_variables():
    check_for_environment_variables(ENVIRONMENT_VARIABLE_NAMES)

    start_date = parse_date_string_to_datetime(os.getenv("START_DATE"))
    end_date = parse_date_string_to_datetime(os.getenv("END_DATE"))
    validate_date_range(start_date, end_date)

    return {
        "START_DATE": start_date,
        "END_DATE": end_date,
        "INTERVAL_IN_DAYS": int(os.getenv("INTERVAL_IN_DAYS")),
        "PATTERN_TEST_FILES": os.getenv("PATTERN_TEST_FILES"),
        "PATTERN_IMPLEMENTATION_FILES": os.getenv(
            "PATTERN_IMPLEMENTATION_FILES"
        ),
        "FILE_EXTENSIONS": os.getenv("FILE_EXTENSIONS"),
    }


def check_for_environment_variables(variables):
    for variable in variables:
        if os.getenv(variable) is None:
            raise ValueError(
                f"Variable {variable} wasn't defined as an environment "
                "variable."
            )
