import sys
import subprocess
import re
from os import path
from datetime import timedelta
from constants.config import load_environment_variables

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
    return (
        subprocess.check_output(
            f"cd '{directory_path}' && git rev-list -1 --before {date} develop",
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )


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


def get_code_duplications_percentage_by_date(
    directory_path, start_date, end_date, interval_in_days
):
    commit_analyzed = ""
    code_duplications_percentage_by_date = []
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        commit_to_analyze = get_commit_by_date(directory_path, date)
        if commit_to_analyze == commit_analyzed:
            break
        subprocess.run(
            f"cd '{directory_path}' && git checkout {commit_to_analyze} --quiet --force",
            shell=True,
            stdout=subprocess.DEVNULL,
            check=True,
        )
        commit_analyzed = commit_to_analyze
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
    header_report = """
        Report Type      | Date       |   Result  
        -----------------|------------|----------
    """
    body_report = ""
    for code_duplication_percentage in get_code_duplications_percentage_by_date(
        directory_path, start_date, end_date, interval_in_days
    ):
        body_report += f"""
        Code Duplication | {code_duplication_percentage['DATE']} | {code_duplication_percentage['CODE_DUPLICATION']}
        -----------------|------------|-----------
        """
    return f"{header_report} {body_report}"


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
