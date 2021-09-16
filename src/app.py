import sys
import os
import json
import csv
from datetime import datetime, timedelta
from constants.config import validate_environment_variables


def get_project_directory():
    console_arguments = sys.argv
    path_analyze_folder = console_arguments[1]
    return path_analyze_folder


def get_dates_between_intervals():
    environment_variables = validate_environment_variables()
    initial_date = datetime.strptime(environment_variables['initial_date'], '%Y-%m-%d')
    end_date = datetime.strptime(environment_variables['end_date'], '%Y-%m-%d')
    interval_days = int(environment_variables['measurement_interval'])
    dates = [initial_date]
    while initial_date <= end_date:
        initial_date = initial_date + timedelta(days=interval_days)
        dates.append(initial_date.strftime('%Y-%m-%d'))
    return dates


def check_commits(path):
    dates = get_dates_between_intervals()
    current_date = datetime.today().strftime('%Y-%m-%d')
    if current_date in dates:
        date_index = dates.index(current_date)
        date_to_analyze = dates[date_index]
        last_commit_id = os.popen('cd {} && git rev-list --before {} -1 master'.format(path, date_to_analyze)).read()
        os.system('cd {} && git show --no-patch --no-notes --pretty=%cs HEAD'.format(path))
        if last_commit_id.strip() != 'd17d910f1e886391bd25aee4cd8ef20dfaa7af83':
            execute_jscpd(path)
    else:
        print('No existe commit')


def execute_jscpd(path_folder):
    complete_jscpd_command = 'jscpd {} --ignore "**/*.json,**/*.yml,**/node_modules/**" --reporters json --output ' \
                             './report/ '.format(path_folder)
    os.system('npm list -g jscpd || npm i -g jscpd@3.3.26')
    print(complete_jscpd_command)
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


if __name__ == '__main__':
    project_path = get_project_directory()
    check_commits(project_path)
    read_reporter_json()
