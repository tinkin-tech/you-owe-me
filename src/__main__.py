import sys
import subprocess
import re
from os import path
from src.constants.config import load_environment_variables
from src.utils.date import get_dates_by_day_interval, subtract_day_to_date
from src.utils.string import (
    remove_whitespace_from_text,
    convert_number_string_to_number_list,
)
from src.utils.git import (
    get_commit_by_date,
    checkout_by_commit_or_branch,
    get_current_branch,
)

global REGEX_TO_FIND_PERCENTAGE_NUMBER
global REGEX_TO_MATCH_WITH_ROW_TOTALS
global DIRECTORY_PATH


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


def get_code_duplication_percentage():
    code_duplication_report = (
        subprocess.check_output(
            f"jscpd '{DIRECTORY_PATH}' --silent --ignore  "
            '"**/*.json,**/*.yml,**/node_modules/**"',
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
    return re.findall(REGEX_TO_FIND_PERCENTAGE_NUMBER, code_duplication_report)[
        0
    ]


def get_report_of_code_lines(
    file_extensions, exclude_test_files=False
):
    return subprocess.check_output(
        f'scc "{DIRECTORY_PATH}" --include-ext="{file_extensions}" '
        f'{"--exclude-dir=test" if exclude_test_files else ""}',
        shell=True,
    ).decode("utf-8")


def get_total_lines_of_code(report_code_lines):
    total_lines_row = remove_whitespace_from_text(
        re.findall(REGEX_TO_MATCH_WITH_ROW_TOTALS, report_code_lines)[0]
    )
    total_lines, blank_lines = convert_number_string_to_number_list(total_lines_row)[1:3]
    return total_lines - blank_lines


def get_implementation_and_test_lines(file_extensions):
    total_lines = get_total_lines_of_code(
        get_report_of_code_lines(file_extensions)
    )
    test_lines = get_total_lines_of_code(
        get_report_of_code_lines(file_extensions, True)
    )
    return {
        "IMPLEMENTATION_LINES": total_lines - test_lines,
        "TEST_LINES": test_lines,
        "TOTAL_LINES": total_lines,
    }


def get_debt_report_by_range_date(
    start_date,
    end_date,
    interval_in_days,
    file_extensions,
):
    debt_report = []
    current_branch = get_current_branch(DIRECTORY_PATH)
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        checkout_by_commit_or_branch(
            DIRECTORY_PATH,
            get_commit_by_date(DIRECTORY_PATH, date, current_branch),
        )
        debt_report.append(
            {
                "DATE": subtract_day_to_date(date, 1),
                "CODE_DUPLICATION": get_code_duplication_percentage(),
                **get_implementation_and_test_lines(
                    file_extensions
                ),
            }
        )
    checkout_by_commit_or_branch(DIRECTORY_PATH, current_branch)
    return debt_report


def format_debt_report(dept_list):
    return (
        "Date;Code Duplication;Implementation Lines;Test Lines; Total Lines\n"
        + "\n".join(
            [
                f"{dept['DATE']};{dept['CODE_DUPLICATION']};"
                f"{dept['IMPLEMENTATION_LINES']};"
                f"{dept['TEST_LINES']};{dept['TOTAL_LINES']}"
                for dept in dept_list
            ]
        )
    )


def main():
    install_debt_report_dependencies()
    env_variables = load_environment_variables()
    debt_report_by_range = get_debt_report_by_range_date(
        env_variables["START_DATE"],
        env_variables["END_DATE"],
        env_variables["INTERVAL_IN_DAYS"],
        env_variables["FILE_EXTENSIONS"],
    )
    print(format_debt_report(debt_report_by_range))


if __name__ == "__main__":
    REGEX_TO_FIND_PERCENTAGE_NUMBER = "\\d+(?:\\.\\d+)?%"
    REGEX_TO_MATCH_WITH_ROW_TOTALS = "(?<=Total)(.*)(?=)"
    DIRECTORY_PATH = get_directory_path_to_analyze()
    main()
