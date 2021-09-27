from datetime import datetime


def format_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date must be before the end date ")
