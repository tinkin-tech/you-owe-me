import sys
import os
import json


def get_directory_path_to_analyze():
    if sys.argv[1]:
        directory_path = sys.argv[1]
        return directory_path
    print('No ha enviado el directorio a ser analizado')


def calculate_code_duplication(directory_path):
    complete_jscpd_command = 'jscpd {} --silent --ignore "**/*.json,**/*.yml,**/node_modules/**" --reporters json' \
                             '--output  ./report/ '.format(directory_path)
    os.system('npm list -g jscpd || npm i -g jscpd@3.3.26')
    os.system(complete_jscpd_command)
    get_total_percentage_repeat_code()


def get_total_percentage_repeat_code():
    json_reporter_path = './report/jscpd-report.json'
    with open(json_reporter_path) as json_file:
        json_object = json.load(json_file)
    total_percentage = json_object['statistics']['total']['percentage']
    return total_percentage


if __name__ == '__main__':
    directory_path_to_analyze = get_directory_path_to_analyze()
    calculate_code_duplication(directory_path_to_analyze)
