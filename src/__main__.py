import sys
import os
import json
import csv
from datetime import datetime
from constants.config import validate_environment_variables


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
    current_date = datetime.today().strftime('%Y-%m-%d')
    with open(json_reporter_path) as json_file:
        json_object = json.load(json_file)
        json_file.close()
    total_percentage = json_object['statistics']['total']['percentage']
    data_to_write = {'fecha': current_date, 'duplicacion': total_percentage}
    write_into_csv(data_to_write)


def write_into_csv(data_to_write):
    file_name = './report/report.csv'
    header = ['fecha', 'duplicacion']
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='UTF8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_to_write)
        csv_file.close()


def report_duplication_between_dates():
    environment_variables = validate_environment_variables()
    print(environment_variables)


if __name__ == '__main__':
    project_path = get_terminal_variables()
    execute_jscpd(project_path)
    read_reporter_json()
