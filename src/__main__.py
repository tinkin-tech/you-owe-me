import sys
import subprocess
import re
from os import path
from datetime import timedelta

sys.path.insert(0, "./")
from src.constants.config import load_environment_variables
from src.utils.utils_git import (
    get_commit_by_date,
    checkout_by_commit_or_branch,
    get_current_branch,
)

REGEX_TO_FIND_PERCENTAGE_NUMBER = "\\d+(?:\\.\\d+)?%"


def has_more_than_one_element(list_):
    return len(list_) > 1


def get_directory_path_to_analyze():
    if not has_more_than_one_element(sys.argv):
        raise Exception(
            "The directory to be analyzed must be passed as an argument"
        )
    if not path.exists(sys.argv[1]):
        raise Exception("The directory to analyze doesn't exist")
    return sys.argv[1]


def install_debt_report_dependencies():
    subprocess.run(
        "npm list -g jscpd || npm i -g jscpd@latest",
        shell=True,
        stdout=subprocess.DEVNULL,
        check=True,
    )


def get_dates_by_day_interval(start_date, end_date, interval_in_days):
    dates_by_day_interval = []
    while start_date <= end_date:
        dates_by_day_interval.append(start_date.strftime("%Y-%m-%d"))
        start_date = start_date + timedelta(days=interval_in_days)
    return dates_by_day_interval


def get_code_duplication_percentage(directory_path):
    code_duplication_report = (
        subprocess.check_output(
            f"jscpd '{directory_path}' --silent --ignore  "
            '"**/*.json,**/*.yml,**/node_modules/**"',
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
    return re.findall(REGEX_TO_FIND_PERCENTAGE_NUMBER, code_duplication_report)[
        0
    ]


def get_code_duplication_by_range_date(
    directory_path,
    start_date,
    end_date,
    interval_in_days,
):
    code_duplications_percentage_by_date = []
    current_branch = get_current_branch(directory_path)
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        checkout_by_commit_or_branch(
            directory_path, get_commit_by_date(directory_path, date)
        )
        code_duplications_percentage_by_date.append(
            {
                "DATE": date,
                "CODE_DUPLICATION": get_code_duplication_percentage(
                    directory_path
                ),
            }
        )
        checkout_by_commit_or_branch(directory_path, current_branch)
    return code_duplications_percentage_by_date


def generate_debt_report(
    directory_path, start_date, end_date, interval_in_days
):
    install_debt_report_dependencies()
    report_body = ""
    for code_duplication_percentage in get_code_duplication_by_range_date(
        directory_path, start_date, end_date, interval_in_days
    ):
        report_body += f"""
        | {code_duplication_percentage['DATE']} |       {code_duplication_percentage['CODE_DUPLICATION']}        |
        -------------|-------------------"""
    return f"""
        -------------|-------------------
        |   Date     | Code Duplication |  
        -------------|-------------------{report_body}
    """


if __name__ == "__main__":
    env_variables = load_environment_variables()
    print(
        generate_debt_report(
            get_directory_path_to_analyze(),
            env_variables["START_DATE"],
            env_variables["END_DATE"],
            env_variables["INTERVAL_IN_DAYS"],
        )
    )
