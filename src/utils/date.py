from datetime import datetime, timedelta


def parse_date_string_to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def format_datetime_to_date_string(datetime_):
    return datetime.strftime(datetime_, "%Y-%m-%d")


def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date must be before the end date ")


def get_dates_by_day_interval(start_date, end_date, interval_in_days):
    dates_by_day_interval = []
    while start_date <= end_date:
        start_date = start_date + timedelta(days=interval_in_days)
        dates_by_day_interval.append(format_datetime_to_date_string(start_date))
    return dates_by_day_interval


def subtract_day_to_date(date_, day_to_subtract):
    return format_datetime_to_date_string(
        parse_date_string_to_datetime(date_) - timedelta(days=day_to_subtract)
    )
