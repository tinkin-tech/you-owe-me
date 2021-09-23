import sys
import subprocess
import re

REGEX_TO_FIND_PERCENTAGE_NUMBER = "\\d+(?:\\.\\d+)?%"


def has_more_than_one_element(dynamic_list):
    return len(dynamic_list) > 1


def get_directory_path_to_analyze():
    if not has_more_than_one_element(sys.argv):
        raise Exception(
            "The directory to be analyzed must be passed as an argument"
        )
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
    code_duplication_percentage = re.findall(
        REGEX_TO_FIND_PERCENTAGE_NUMBER, code_duplication_report
    )
    return code_duplication_percentage[0]


def generate_debt_report(directory_path):
    install_debt_report_dependencies()
    return f"""
    Report Type      | Result
    -----------------|-----------
    Code Duplication | {get_code_duplication_percentage(directory_path)}
    """


if __name__ == "__main__":
    print(generate_debt_report(get_directory_path_to_analyze()))
