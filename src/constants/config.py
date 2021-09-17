from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()


def load_environment_variables():
    measurement_start_date = os.getenv("MEASUREMENT_START_DATE")
    measurement_end_date = os.getenv("MEASUREMENT_END_DATE")
    measurement_intervals = os.getenv("MEASUREMENT_INTERVAL")
    regex_test_files = os.getenv("REGEX_TEST_FILES")
    regex_implementation_files = os.getenv("REGEX_IMPLEMENTATION_FILES")

    if measurement_start_date is None or measurement_end_date is None or measurement_intervals is None \
            or regex_test_files is None or regex_implementation_files is None:
        raise ValueError("Environment variables haven't been set")

    if measurement_start_date > measurement_end_date:
        raise ValueError("Initial date must be less than end date")

    return {
        'MEASUREMENT_START_DATE': datetime.strptime(measurement_start_date, '%Y-%m-%d'),
        'MEASUREMENT_END_DATE': datetime.strptime(measurement_end_date, '%Y-%m-%d'),
        'MEASUREMENT_INTERVAL': int(measurement_intervals),
        'REGEX_TEST_FILES': regex_test_files,
        'REGEX_IMPLEMENTATION_FILES': regex_implementation_files,
    }
