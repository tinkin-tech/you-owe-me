import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


def load_environment_variables():
    # TODO: Primera refactorización (abstraer a un función que va a iterar cada variable de entorno)
    # if start_date is None or end_date is None or interval_in_days is None:
    #    raise ValueError("Environment variables haven't been given")

    # TODO: Segunda refactorización (abstraer el formateo de las fechas a util)
    start_date = datetime.strptime(os.getenv("START_DATE"), "%Y-%m-%d")
    end_date = datetime.strptime(os.getenv("END_DATE"), "%Y-%m-%d")

    # TODO: Tercera refactorización (es de otro método la responsabilidad de validar las fechas)
    if start_date > end_date:
        raise ValueError("The initial date must be before the end date")

    # TODO: Cuarta refactorización (por revisar)
    return {
        "START_DATE": start_date,
        "END_DATE": end_date,
        "INTERVAL_IN_DAYS": int(os.getenv("INTERVAL_IN_DAYS")),
    }
