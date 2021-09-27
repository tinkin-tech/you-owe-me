import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


def load_environment_variables():
    start_date = os.getenv("START_DATE")
    end_date = os.getenv("END_DATE")
    interval_in_days = os.getenv("INTERVAL_IN_DAYS")

    if start_date is None or end_date is None or interval_in_days is None:
        raise ValueError("Environment variables haven't been given")

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if start_date > end_date:
        raise ValueError("The initial date must be before the end date")

    return {
        'START_DATE': start_date,
        'END_DATE': end_date,
        'INTERVAL_IN_DAYS': int(interval_in_days),
    }
