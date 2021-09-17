import sys
import os
import re
import csv
from datetime import datetime, timedelta
from constants.config import load_environment_variables

environment_variables = load_environment_variables()


def get_directory_path_to_analyze():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        return directory_path
    raise Exception("The directory to be analyzed hasn't been sent")


def get_measurement_dates_between_intervals():
    measurement_start_date = environment_variables['MEASUREMENT_START_DATE']
    measurement_end_date = environment_variables['MEASUREMENT_END_DATE']
    measurement_intervals = environment_variables['MEASUREMENT_INTERVAL']
    measurement_dates = [measurement_start_date.strftime('%Y-%m-%d')]
    while measurement_start_date <= measurement_end_date:
        measurement_start_date = measurement_start_date + timedelta(days=measurement_intervals)
        measurement_dates.append(measurement_start_date.strftime('%Y-%m-%d'))
    return measurement_dates


def check_duplicate_code_commits(directory_path):
    dates = get_measurement_dates_between_intervals()
    commits = []
    for commit_date in dates:
        commit_id = os.popen('cd {} && git rev-list --before {} -1 master'.format(directory_path, commit_date)).read()
        if commit_id in commits:
            print('Repeated commit')
            break
        commits.append(commit_id)
        os.system('cd {} && git checkout {} --quiet'.format(directory_path, commit_id.strip()))
        calculate_code_duplication(directory_path, commit_date)


def calculate_code_duplication(directory_path, commit_date):
    regex_files = environment_variables['REGEX_IMPLEMENTATION_FILES']
    complete_jscpd_command = 'jscpd {} --silent --ignore "**/*.json,**/*.yml,**/node_modules/**" ' \
                             '--pattern "{}"'.format(directory_path, regex_files)
    os.system('npm list -g jscpd || npm i -g jscpd@3 --silent')
    jscpd_response = os.popen(complete_jscpd_command).read()
    total_percentage_duplicated = re.findall('\\d+(?:\\.\\d+)?%', jscpd_response.strip())[0]
    data_to_write_csv = {'date': commit_date, 'duplication': total_percentage_duplicated}
    write_into_csv_report(data_to_write_csv)


def write_into_csv_report(data_to_write):
    file_name = './report/report.csv'
    header = ['date', 'duplication']
    file_exists = os.path.isfile(file_name)
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    with open(file_name, 'a', encoding='UTF8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_to_write)


if __name__ == '__main__':
    directory_path_to_analyze = get_directory_path_to_analyze()
    check_duplicate_code_commits(directory_path_to_analyze)
