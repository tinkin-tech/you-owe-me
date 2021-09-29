import sys
import subprocess
import re
from os import path
from src.constants.config import load_environment_variables
from src.utils.date import get_dates_by_day_interval
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


def get_report_of_code_lines(
    directory_path, file_extensions, analyze_test_files=False
):
    return subprocess.check_output(
        f'scc "{directory_path}" --include-ext="{file_extensions}" '
        f'{"--exclude-dir=test" if analyze_test_files else ""}',
        shell=True,
    ).decode("utf-8")


def get_total_lines_of_code(report_code_lines):
    text_total_information_lines = remove_whitespace_from_text(
        re.findall(REGEX_TO_MATCH_WITH_ROW_TOTALS, report_code_lines)[0]
    )
    list_total_information_lines = convert_text_to_number_list(
        text_total_information_lines
    )[1:3]
    return list_total_information_lines[0] - list_total_information_lines[1]


def get_lines_implementation_and_test(directory_path, file_extensions):
    total_lines = get_total_lines_of_code(
        get_report_of_code_lines(directory_path, file_extensions)
    )
    test_lines = get_total_lines_of_code(
        get_report_of_code_lines(directory_path, file_extensions, True)
    )
    return {
        "IMPLEMENTATION_LINES": total_lines - test_lines,
        "TEST_LINES": test_lines,
        "TOTAL_LINES": total_lines,
    }


def get_debts_information(
    directory_path,
    start_date,
    end_date,
    interval_in_days,
    file_extensions,
):
    debts_information = []
    current_branch = get_current_branch(directory_path)
    for date in get_dates_by_day_interval(
        start_date, end_date, interval_in_days
    ):
        checkout_by_commit_or_branch(
            directory_path,
            get_commit_by_date(directory_path, date, current_branch),
        )

        debts_information.append(
            {
                "DATE": date,
                "CODE_DUPLICATION": get_code_duplication_percentage(
                    directory_path
                ),
                **get_lines_implementation_and_test(
                    directory_path, file_extensions
                ),
            }
        )
    checkout_by_commit_or_branch(directory_path, current_branch)
    return code_duplications_percentage_by_date


def format_debt_report(code_duplication_list):
    return "Date;Code Duplication\n" + "\n".join(
        [
            f"{code_duplication['DATE']};{code_duplication['CODE_DUPLICATION']}"
            for code_duplication in code_duplication_list
        ]
    )


def main():
    install_debt_report_dependencies()
    env_variables = load_environment_variables()
    code_duplication_by_range = get_code_duplication_by_range_date(
        get_directory_path_to_analyze(),
        env_variables["START_DATE"],
        env_variables["END_DATE"],
        env_variables["INTERVAL_IN_DAYS"],
    )
    print(format_debt_report(code_duplication_by_range))


if __name__ == "__main__":
    main()
