import sys
import os
import json


def get_terminal_variables():
    console_arguments = sys.argv
    path_analyze_folder = console_arguments[1]
    return path_analyze_folder


def execute_jscpd(path_folder):
    complete_command = 'jscpd {} --ignore "**/*.json,**/*.yml" --reporters json --output ./report/ '.format(path_folder)
    os.system('npm i jscpd -g')
    os.system(complete_command)


def read_reporter_json():
    json_reporter_path = './report/jscpd-report.json'
    with open(json_reporter_path) as json_file:
        json_object = json.load(json_file)
        json_file.close()
    total_lines = json_object['statistics']['total']['lines']
    total_percentage = json_object['statistics']['total']['percentage']
    total_duplicated_lines = json_object['statistics']['total']['duplicatedLines']
    print(total_percentage, total_lines, total_duplicated_lines)


if __name__ == '__main__':
    path = get_terminal_variables()
    execute_jscpd(path)
    read_reporter_json()
