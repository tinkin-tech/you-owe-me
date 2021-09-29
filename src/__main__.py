import sys
import subprocess
import re
from os import path
from src.constants.config import load_environment_variables
from src.utils.file import write_to_csv_report
from src.utils.date import get_dates_by_day_interval
from src.utils.git import (
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
            directory_path,
            get_commit_by_date(directory_path, date, current_branch),
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


def format_debt_report(code_duplication_list):
    return f"Date;Code Duplication\n" + "\n".join(
        [f"{code_duplication['DATE']};{code_duplication['CODE_DUPLICATION']}"
        for code_duplication in code_duplication_list]
    )


def main():
    env_variables = load_environment_variables()
    install_debt_report_dependencies()
    print(
        format_debt_report(
            get_code_duplication_by_range_date(
                get_directory_path_to_analyze(),
                env_variables["START_DATE"],
                env_variables["END_DATE"],
                env_variables["INTERVAL_IN_DAYS"],
            )
        )
    )


if __name__ == "__main__":
    main()
