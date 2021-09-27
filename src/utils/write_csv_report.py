import os
import csv


def write_report_csv(data_to_write):
    report_directory = "./report/report.csv"
    header = ["DATE", "CODE_DUPLICATION"]
    file_exists = os.path.isfile(report_directory)
    if not os.path.exists(os.path.dirname(report_directory)):
        os.makedirs(os.path.dirname(report_directory))
    with open(report_directory, "a", encoding="UTF8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_to_write)
