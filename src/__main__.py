import sys
import subprocess
import re
from os import path
from datetime import timedelta
from constants.config import load_environment_variables
from utils.write_csv_report import write_report_csv

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
        start_date = start_date + timedelta(days=interval_in_days)
        dates_by_day_interval.append(start_date.strftime("%Y-%m-%d"))
    return dates_by_day_interval


def get_commit_by_date(directory_path, date):
    commit = (
        subprocess.check_output(
            f"cd '{directory_path}' && git rev-list -1 --before {date} master",
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
    subprocess.run(
        f"cd '{directory_path}' && git checkout {commit} --quiet --force",
        shell=True,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    return commit


def get_code_duplication_percentage(directory_path):
    code_duplication_report = (
        subprocess.check_output(
            f"jscpd '{directory_path}' --silent --ignore  "
            '"**/*.json,**/*.yml,**/node_modules/**" --pattern "**/*.{js,jsx}"',
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
    return re.findall(REGEX_TO_FIND_PERCENTAGE_NUMBER, code_duplication_report)[
        0
    ]


def get_debt_report_by_date(
    directory_path, start_date, end_date, interval_in_days
):
    previous_analyzed_commit = ""
    code_duplications_percentage_by_date = []
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        analyzed_commit = get_commit_by_date(directory_path, date)
        if analyzed_commit == previous_analyzed_commit:
            break
        previous_analyzed_commit = analyzed_commit
        code_duplications_percentage_by_date.append(
            {
                "DATE": date,
                "CODE_DUPLICATION": get_code_duplication_percentage(
                    directory_path
                ),
            }
        )
    return code_duplications_percentage_by_date


def generate_debt_report(
    directory_path, start_date, end_date, interval_in_days
):
    install_debt_report_dependencies()
    report_header = """
        -------------|-------------------
        |   Date     | Code Duplication |  
        -------------|-------------------"""
    report_body = ""
    for code_duplication_percentage in get_debt_report_by_date(
        directory_path, start_date, end_date, interval_in_days
    ):
        report_body += f"""
        | {code_duplication_percentage['DATE']} |     {code_duplication_percentage['CODE_DUPLICATION']}       |
        -------------|-------------------"""
        write_report_csv(code_duplication_percentage)
    return f"{report_header}{report_body}"


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
