import sys
import subprocess
import re


def have_more_than_one_element(list):
    return len(list) > 1


def get_element_by_index(list, index, default_value):
    try:
        return list[index]
    except IndexError:
        return default_value


def get_directory_path_to_analyze():
    if not have_more_than_one_element(sys.argv):
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
    return get_element_by_index(
        re.findall("\\d+(?:\\.\\d+)?%", code_duplication_report), 0, "0%"
    )


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
