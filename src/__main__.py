import sys
import subprocess
import re


def get_directory_path_to_analyze():
    if len(sys.argv) > 1:
        return sys.argv[1]
    raise Exception("The directory to be analyzed must be passed as argument")


def install_debt_report_dependencies():
    subprocess.run(
        "npm list -g jscpd || npm i -g jscpd@3.3.26",
        shell=True,
        stdout=subprocess.DEVNULL,
    )


def get_code_duplication_percentage(directory_path):
    code_duplication_report = subprocess.check_output(
        "jscpd {} --silent --ignore  "
        '"**/*.json,**/*.yml,**/node_modules/**"'.format(directory_path),
        shell=True,
    ).decode("utf-8").strip()
    return re.findall(
        "\\d+(?:\\.\\d+)?%", code_duplication_report
    )[0]


def generate_debt_report():
    install_debt_report_dependencies()
    print(
        """
    Report Type      | Result
    -----------------|-----------
    Code Duplication | %s
    """
        % get_code_duplication_percentage(get_directory_path_to_analyze())
    )


if __name__ == "__main__":
    generate_debt_report()
