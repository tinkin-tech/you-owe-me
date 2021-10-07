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

REGEX_TO_FIND_PERCENTAGE_NUMBER = "\\d+(?:\\.\\d+)?%"
REGEX_TO_MATCH_WITH_ROW_TOTALS = "(?<=Total)(.*)(?=)"


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


def get_report_of_code_lines(directory_path, file_extensions, exclude_test):
    return subprocess.check_output(
        f'scc "{directory_path}" --include-ext="{file_extensions}" '
        f"{'--exclude-dir=test' if exclude_test else ''}",
        shell=True,
    ).decode("utf-8")


def get_report_implementation_lines(directory_path, file_extensions):
    return get_report_of_code_lines(directory_path, file_extensions, True)


def get_report_total_lines(directory_path, file_extensions):
    return get_report_of_code_lines(directory_path, file_extensions, False)


def get_total_lines_of_code(report_code_lines):
    total_lines_row = remove_whitespace_from_text(
        re.findall(REGEX_TO_MATCH_WITH_ROW_TOTALS, report_code_lines)[0]
    )
    total_lines, blank_lines = convert_number_string_to_number_list(
        total_lines_row
    )[1:3]
    return total_lines - blank_lines


def get_implementation_and_test_lines(directory_path, file_extensions, type_):
    total_lines = get_total_lines_of_code(
        get_report_total_lines(directory_path, file_extensions)
    )
    implementation_lines = get_total_lines_of_code(
        get_report_implementation_lines(directory_path, file_extensions)
    )
    return {
        "implementation_lines": implementation_lines,
        "test_lines": total_lines - implementation_lines,
        "total_lines": total_lines,
    }.get(type_)


def get_debt_report_by_range_date(
    directory_path,
    file_extensions,
    start_date,
    end_date,
    interval_in_days,
):
    debt_report = []
    current_branch = get_current_branch(directory_path)
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        checkout_by_commit_or_branch(
            directory_path,
            get_commit_by_date(directory_path, date, current_branch),
        )
        debt_report.append(
            {
                "DATE": subtract_day_to_date(date, 1),
                "CODE_DUPLICATION": get_code_duplication_percentage(
                    directory_path
                ),
                "IMPLEMENTATION_LINES": get_implementation_and_test_lines(
                    directory_path, file_extensions, "implementation_lines"
                ),
                "TEST_LINES": get_implementation_and_test_lines(
                    directory_path, file_extensions, "test_lines"
                ),
                "TOTAL_LINES": get_implementation_and_test_lines(
                    directory_path, file_extensions, "total_lines"
                ),
            }
        )
    checkout_by_commit_or_branch(directory_path, current_branch)
    return debt_report


def format_debt_report(debt_list):
    return (
        "Date;Code Duplication;Implementation Lines;Test Lines; Total Lines\n"
        + "\n".join(
            [
                f"{debt['DATE']};{debt['CODE_DUPLICATION']};"
                f"{debt['IMPLEMENTATION_LINES']};"
                f"{debt['TEST_LINES']};{debt['TOTAL_LINES']}"
                for debt in debt_list
            ]
        )
    )


def main():
    install_debt_report_dependencies()
    env_variables = load_environment_variables()
    debt_report_by_range = get_debt_report_by_range_date(
        get_directory_path_to_analyze(),
        env_variables["FILE_EXTENSIONS"],
        env_variables["START_DATE"],
        env_variables["END_DATE"],
        env_variables["INTERVAL_IN_DAYS"],
    )
    print(format_debt_report(debt_report_by_range))


if __name__ == "__main__":
    main()
