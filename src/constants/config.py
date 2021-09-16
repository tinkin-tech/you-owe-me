from dotenv import load_dotenv
import os

load_dotenv()

MEASUREMENT_START_DATE = os.getenv("MEASUREMENT_START_DATE")
MEASUREMENT_END_DATE = os.getenv("MEASUREMENT_END_DATE")
MEASUREMENT_INTERVAL = os.getenv("MEASUREMENT_INTERVAL")


def validate_environment_variables():
    if MEASUREMENT_START_DATE is None or MEASUREMENT_END_DATE is None or MEASUREMENT_INTERVAL is None:
        raise ValueError('No se ha seteado las variables de entorno')
    return {
        'initial_date': MEASUREMENT_START_DATE,
        'end_date': MEASUREMENT_END_DATE,
        'measurement_interval': MEASUREMENT_INTERVAL,
    }
