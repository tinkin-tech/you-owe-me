from os import path, makedirs
import csv


def write_to_csv_report(data_to_write):
    file_name = "./report/report.csv"
    csv_header = ["DATE", "CODE_DUPLICATION"]
    exist_file = path.isfile(file_name)
    if not path.exists(path.dirname(file_name)):
        makedirs(path.dirname(file_name))
    with open(file_name, "a", encoding="UTF8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=csv_header)
        if not exist_file:
            writer.writeheader()
        writer.writerow(data_to_write)
