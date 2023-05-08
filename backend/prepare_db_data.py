import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.load_data import load_data
from scripts.preprocessing import (
    convert_and_format_date_columns_to_string,
    convert_reporting_column,
    convert_to_csv,
    extract_technical_efficiency_value,
    filter_by_date_format,
    year_to_last_day,
)

PATH_TO_EXCEL_FILES = Path(__file__).resolve().parent.parent / "data"
PATH_TO_OUTPUT_FILE = Path(__file__).resolve().parent / "app" / "data" / "output.csv"

COLUMNS_TO_KEEP = [
    "Name",
    "Ship type",
    "Reporting Period",
    "DoC issue date",
    "DoC expiry date",
    "Annual average CO₂ emissions per distance [kg CO₂ / n mile]",
    "Total CO₂ emissions [m tonnes]",
    "Technical efficiency",
]


def configure_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()],
    )


def load_and_filter_data(data_path, columns_to_keep):
    """
    Load data and filter it according to given column names.
    
    Args:
        data_path (Path): The path to the data file.
        columns_to_keep (list): A list of column names to keep.
        
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    df = load_data(data_path)
    df = df[columns_to_keep]
    return df


def process_data(df):
    """
    Process data by applying various transformations.
    
    Args:
        df (pd.DataFrame): The DataFrame to process.
        
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    df = extract_technical_efficiency_value(df, "Technical efficiency", "Technical efficiency")
    df = df.dropna(subset=["Technical efficiency"])
    df = df[~df["Technical efficiency"].isin([0.0, 0])]
    column1 = "Annual average CO₂ emissions per distance [kg CO₂ / n mile]"
    df = df.loc[df[column1] != "Division by zero!"]
    df[column1] = df[column1].astype(float)
    df = convert_reporting_column(df, "Reporting Period", year_to_last_day, "%d/%m/%Y")
    df = filter_by_date_format(df, "DoC issue date", r"^\d{2}/\d{2}/\d{4}$")
    df = convert_and_format_date_columns_to_string(df)
    return df


def main():
    """Main function to run the script."""
    configure_logging()
    df = load_and_filter_data(PATH_TO_EXCEL_FILES, COLUMNS_TO_KEEP)
    df = process_data(df)
    convert_to_csv(df, PATH_TO_OUTPUT_FILE)
    logging.info("Data successfully processed")
    logging.info("DataFrame's content:\n" + str(df.head()))


if __name__ == "__main__":
    main()
