import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_xlsx_files(folder_path):
    """
    Get a list of all .xlsx files in the specified folder path.
    
    Args:
        folder_path (Path): A pathlib.Path object representing the folder path.
    
    Returns:
        list: A list of pathlib.Path objects representing the .xlsx files in the folder.
    """
    xlsx_files = [file for file in folder_path.iterdir() if file.suffix == ".xlsx"]
    logging.info(f"Found {len(xlsx_files)} .xlsx files in {folder_path}")
    return xlsx_files


def read_and_combine_xlsx_files(xlsx_files, header):
    """
    Read and combine the contents of .xlsx files into a single Pandas DataFrame.
    
    Args:
        xlsx_files (list): A list of pathlib.Path objects representing the .xlsx files.
        header (int): The row index to use as the column names in the DataFrame.
    
    Returns:
        pd.DataFrame: A combined DataFrame containing data from all .xlsx files.
    """
    dfs = []

    for file in xlsx_files:
        logging.info(f"Reading {file}")
        temp_df = pd.read_excel(file, header=header)
        dfs.append(temp_df)

    combined_df = pd.concat(dfs, ignore_index=True)
    logging.info(f"Combined {len(xlsx_files)} .xlsx files into a single DataFrame")
    return combined_df


def load_data(folder_path):
    """
    Load data from .xlsx files in the specified folder path and combine them into a single DataFrame.
    
    Args:
        folder_path (str): The folder path containing .xlsx files.
    
    Returns:
        pd.DataFrame: A combined DataFrame containing data from all .xlsx files.
    """
    folder_path = Path(folder_path)
    xlsx_files = get_xlsx_files(folder_path)
    combined_df = read_and_combine_xlsx_files(xlsx_files, header=2)
    return combined_df


if __name__ == "__main__":
    your_folder_path = "../data/"
    combined_df = load_data(your_folder_path)
    print(combined_df)
