from datetime import datetime, timedelta


def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date must be before the end date ")


def get_dates_by_day_interval(start_date, end_date, interval_in_days):
    dates_by_day_interval = list()
    while start_date <= end_date:
        dates_by_day_interval.append(start_date.strftime("%Y-%m-%d"))
        start_date = start_date + timedelta(days=interval_in_days)
    return dates_by_day_interval
