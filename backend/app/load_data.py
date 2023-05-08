import logging

import pandas as pd
from app.models.models import Ship

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

col_names = {
    "Name": "name",
    "Ship type": "ship_type",
    "Reporting Period": "reporting_period",
    "DoC issue date": "doc_issue_date",
    "DoC expiry date": "doc_expiry_date",
    "Annual average CO₂ emissions per distance [kg CO₂ / n mile]": "annual_average_co2_emissions",
    "Total CO₂ emissions [m tonnes]": "total_co2_emissions",
    "Technical efficiency": "technical_efficiency",
}


def load_csv(file_path, col_names=col_names):
    """
    Load a CSV file and convert it into a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file.
    """
    df = pd.read_csv(file_path)
    df = df.rename(columns=col_names)
    records = df.to_dict("records")
    return records


async def insert_records(records):
    """
    Asynchronously insert a list of records into the Ship database model.

    Args:
        records (list): A list of dictionaries, where each dictionary represents a row in the Ship database model.

    Returns:
        None
    """

    try:
        await Ship.bulk_create([Ship(**record) for record in records])
    except Exception as e:
        logging.error(f"Error inserting records: {e}")
        raise

