import sys
import subprocess
import re

REGEX_TO_FIND_PERCENTAGE_NUMBER = "\\d+(?:\\.\\d+)?%"


def has_more_than_one_element(list):
    return len(list) > 1


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
    )


def get_code_duplication_percentage(directory_path):
    code_duplication_report = (
        subprocess.check_output(
            "jscpd '{}' --silent --ignore  "
            '"**/*.json,**/*.yml,**/node_modules/**"'.format(directory_path),
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
    code_duplication_percentage = re.findall(REGEX_TO_FIND_PERCENTAGE_NUMBER, code_duplication_report)
    if not has_more_than_one_element(code_duplication_percentage):
        raise Exception(
            "There isn't JSCPD result for the submitted directory"
        )
    return code_duplication_percentage[0]


def generate_debt_report():
    install_debt_report_dependencies()
    print(
        """
    Report Type      | Result
    -----------------|-----------
    Code Duplication | {}
    """.format(
            get_code_duplication_percentage(get_directory_path_to_analyze())
        )
    )


if __name__ == "__main__":
    generate_debt_report()
