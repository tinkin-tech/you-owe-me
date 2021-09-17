import sys
import os
import re


def get_directory_path_to_analyze():
    if len(sys.argv[1]) > 1:
        directory_path = sys.argv[1]
        return directory_path
    raise Exception("The directory to be analyzed wasn't sent")


def calculate_code_duplication(directory_path):
    complete_jscpd_command = 'jscpd {} --silent --ignore "**/*.json,**/*.yml,**/node_modules/**" ' \
                             ''.format(directory_path)
    os.system('npm list -g jscpd || npm i -g jscpd@3.3.26')
    jscpd_response = os.popen(complete_jscpd_command).read()
    total_percentage_duplicated = re.findall('\\d+(?:\\.\\d+)?%', jscpd_response.strip())[0]
    print(total_percentage_duplicated)  # este valor se usa para escribir en csv


if __name__ == '__main__':
    directory_path_to_analyze = get_directory_path_to_analyze()
    calculate_code_duplication(directory_path_to_analyze)
