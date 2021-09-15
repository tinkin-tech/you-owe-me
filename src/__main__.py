import sys
import os
import json


def get_terminal_variables():
    console_arguments = sys.argv
    path_analyze_folder = console_arguments[1]
    return path_analyze_folder


def execute_jscpd(path_folder):
    complete_jscpd_command = 'jscpd {} --ignore "**/*.json,**/*.yml,**/node_modules/**" --reporters json --output ' \
                       './report/ '.format(path_folder)
    os.system('npm list -g jscpd || npm i -g jscpd@3.3.26')
    os.system(complete_jscpd_command)


def read_reporter_json():
    json_reporter_path = './report/jscpd-report.json'
    with open(json_reporter_path) as json_file:
        json_object = json.load(json_file)
        json_file.close()
    total_percentage = json_object['statistics']['total']['percentage']
    return total_percentage


if __name__ == '__main__':
    project_path = get_terminal_variables()
    execute_jscpd(project_path)
    read_reporter_json()
