import sys
import os
import re
import csv
import subprocess
from datetime import datetime, timedelta
from constants.config import load_environment_variables

environment_variables = load_environment_variables()


def get_directory_path_to_analyze():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        return directory_path
    raise Exception("The directory to be analyzed hasn't been given")


def get_measurement_dates_between_intervals():
    measurement_start_date = environment_variables['MEASUREMENT_START_DATE']
    measurement_end_date = environment_variables['MEASUREMENT_END_DATE']
    measurement_intervals = environment_variables['MEASUREMENT_INTERVAL']
    measurement_dates = [measurement_start_date.strftime('%Y-%m-%d')]
    while measurement_start_date <= measurement_end_date:
        measurement_start_date = measurement_start_date + timedelta(days=measurement_intervals)
        measurement_dates.append(measurement_start_date.strftime('%Y-%m-%d'))
    return measurement_dates


def get_percentages_duplicate_code_by_commits(directory_path):
    dates = get_measurement_dates_between_intervals()
    commit_id_analyzed = ''
    percentages_duplicate_code = []
    for commit_date in dates:
        get_commit_id = 'cd {} && git rev-list -1 --before {} master ' \
                        ''.format(directory_path, commit_date)
        commit_id = subprocess.check_output(get_commit_id, shell=True).decode('utf-8')
        if commit_id == commit_id_analyzed:
            break
        commit_id_analyzed = commit_id
        switch_to_commit = 'cd {} && git checkout {} --quiet --force'.format(directory_path, commit_id.strip())
        subprocess.run(switch_to_commit, shell=True)
        percentages_duplicate_code.append(get_percentage_duplicate_code(directory_path))
    return percentages_duplicate_code


def get_percentage_duplicate_code(directory_path):
    regex_implementation_files = environment_variables['REGEX_IMPLEMENTATION_FILES']
    get_code_duplication = 'jscpd {} --silent --ignore "**/*.json,**/*.yml,**/node_modules/**" ' \
                           '--pattern "{}"'.format(directory_path, regex_implementation_files)
    subprocess.run('npm list -g jscpd || npm i -g jscpd@3', shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)
    output = subprocess.check_output(get_code_duplication, shell=True).decode('utf-8')
    # the regular expression find the numbers with percentage
    percentage_duplicated = re.findall('\\d+(?:\\.\\d+)?%', output.strip())[0]
    return percentage_duplicated


def get_code_coverage_report(directory_path):
    regex_implementation_files = environment_variables['REGEX_IMPLEMENTATION_FILES']
    generate_coverage_report = 'cd {} && npx jest --coverage ' \
                               '--coverageReporters="json-summary" --collectCoverageFrom={}' \
                               ''.format(directory_path, regex_implementation_files)
    get_head_coverage_report = 'cd {} && cat coverage/coverage-summary.json | head -1'.format(directory_path)
    subprocess.run(generate_coverage_report, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    output = subprocess.check_output(get_head_coverage_report, shell=True).decode('utf-8')
    # the regular expression looks for the deepest value nested inside a json, and returns it (return information
    summary_lines_code = re.findall('(?<=\{)\s*[^{]*?(?=[\}])', output.strip())[0]
    percentage_code_coverage = summary_lines_code.split(',')[3]
    print(int(filter(str.isdigit, percentage_code_coverage)))
    print(type(percentage_code_coverage))


def write_csv_report(data_to_write):
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
    get_percentages_duplicate_code_by_commits(get_directory_path_to_analyze())
