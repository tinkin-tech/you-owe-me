import sys
import os
import json
import csv
from datetime import datetime, timedelta
from constants.config import validate_environment_variables


def get_directory_path_to_analyze():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        return directory_path
    print('No ha enviado el directorio a ser analizado')


def get_dates_between_intervals():
    environment_variables = validate_environment_variables()
    end_date = datetime.strptime(environment_variables['end_date'], '%Y-%m-%d')
    initial_date = datetime.strptime(environment_variables['initial_date'], '%Y-%m-%d')
    interval_days = int(environment_variables['measurement_interval'])
    dates = [initial_date.strftime('%Y-%m-%d')]
    while initial_date <= end_date:
        initial_date = initial_date + timedelta(days=interval_days)
        dates.append(initial_date.strftime('%Y-%m-%d'))
    return dates


def check_duplicate_code_commits(directory_path):
    commits_dates = get_dates_between_intervals()
    commits = []
    for commit_date in commits_dates:
        commit_id = os.popen('cd {} && git rev-list --before {} -1 master'.format(directory_path, commit_date)).read()
        if commit_id in commits:
            print('Commit repetido')
            break
        commits.append(commit_id)
        os.system('cd {} && git checkout {}'.format(directory_path, commit_id.strip()))
        calculate_code_duplication(directory_path)
        get_total_percentage_repeat_code(commit_date)


def calculate_code_duplication(directory_path):
    complete_jscpd_command = 'jscpd {} --silent --ignore "**/*.json,**/*.yml,**/node_modules/**" --reporters json ' \
                             '--output  ./report/ '.format(directory_path)
    os.system('npm list -g jscpd || npm i -g jscpd@3.3.26')
    os.system(complete_jscpd_command)


def get_total_percentage_repeat_code(commit_date):
    json_reporter_path = './report/jscpd-report.json'
    with open(json_reporter_path) as json_file:
        json_object = json.load(json_file)
    total_percentage = json_object['statistics']['total']['percentage']
    data_to_write = {'fecha': commit_date, 'duplicacion': total_percentage}
    write_into_csv_report(data_to_write)
    os.system('rm {}'.format(json_reporter_path))


def write_into_csv_report(data_to_write):
    file_name = './report/report.csv'
    header = ['fecha', 'duplicacion']
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='UTF8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_to_write)
        csv_file.close()


if __name__ == '__main__':
    directory_path_to_analyze = get_directory_path_to_analyze()
    check_duplicate_code_commits(directory_path_to_analyze)
