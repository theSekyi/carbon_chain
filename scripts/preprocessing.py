import datetime
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def calculate_missing_percentage(df):
    """
    Calculate the missing percentage for each column in a DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.Series: A pandas Series containing the missing percentage for each column.
    """
    logging.info("Calculating missing percentage for each column in the DataFrame")
    return (df.isna().sum() / len(df)) * 100


def calculate_annual_emissions(df):
    """
    Calculate the annual total CO₂ emissions from the input DataFrame.
    
    Args:
        df (pd.DataFrame): A pandas DataFrame containing the columns 'Reporting Period' and 'Total CO₂ emissions [m tonnes]'.
    
    Returns:
        pd.DataFrame: A new DataFrame containing the annual total CO₂ emissions.
    """
    df["Year"] = df["Reporting Period"].astype("category")
    annual_emissions = df.groupby("Year")["Total CO₂ emissions [m tonnes]"].sum().reset_index()
    return annual_emissions


def missing_percentage_dataframe(df):
    """
    Create a DataFrame containing the missing percentage for each column in the input DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: A new DataFrame containing the missing percentage for each column.
    """
    logging.info("Creating a DataFrame containing the missing percentage for each column")
    missing_percentage = calculate_missing_percentage(df)
    return pd.DataFrame(missing_percentage, columns=["Missing Percentage"])


def sort_by_missing_percentage(df):
    """
    Sort a DataFrame by the 'Missing Percentage' column in descending order.
    
    Args:
        df (pd.DataFrame): The input DataFrame, which must have a 'Missing Percentage' column.
    
    Returns:
        pd.DataFrame: A sorted DataFrame with columns sorted by 'Missing Percentage' in descending order.
    """
    logging.info("Sorting DataFrame by 'Missing Percentage' column in descending order")
    return df.sort_values(by="Missing Percentage", ascending=False)


def drop_columns_above_threshold(original_df, missing_percentage_df, threshold):
    """
    Drop columns from the original DataFrame if their missing percentage is above the given threshold.
    
    Args:
        original_df (pd.DataFrame): The input DataFrame from which columns need to be dropped.
        missing_percentage_df (pd.DataFrame): A DataFrame containing the missing percentage for each column.
        threshold (float): The threshold percentage for dropping columns.
    
    Returns:
        pd.DataFrame: A new DataFrame with columns dropped based on the threshold.
    """
    logging.info(f"Dropping columns with missing percentage above {threshold}%")
    columns_to_drop = missing_percentage_df[missing_percentage_df["Missing Percentage"] > threshold].index
    return original_df.drop(columns=columns_to_drop)


def calculate_correlation(
    data, method="pearson", column1="Total fuel consumption [m tonnes]", column2="Total CO₂ emissions [m tonnes]"
):
    """
    Calculate the correlation coefficient between 'Total fuel consumption [m tonnes]'
    and 'Total CO₂ emissions [m tonnes]' columns in the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame containing the columns.
        method (str, optional): The correlation method. Defaults to 'pearson'.

    Returns:
        float: The correlation coefficient.
    """
    correlation = data[column1].corr(data[column2], method=method)
    return correlation


def extract_technical_efficiency_value(df, source_column, target_column):
    """
    Extract the numeric value from the source_column and create a new column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the source column.
        source_column (str): The name of the source column containing the values to extract.
        target_column (str): The name of the new column to create with the extracted values.
    """
    df[target_column] = df[source_column].str.extract("(\d+\.\d+)").astype(float)
    return df


def group_by_ship_type(df, column):
    """
    Group the DataFrame by 'Ship type' and calculate the mean of the specified column for each group.

    Args:
        df (pd.DataFrame): The input DataFrame containing the 'Ship type' column.
        column (str): The name of the column to calculate the mean.

    Returns:
        pd.DataFrame: A new DataFrame with the mean of the specified column for each ship type.
    """
    return df.groupby("Ship type")[column].mean().reset_index()


def year_to_last_day(year):
    """
    Convert a given year to the last day of that year (December 31st).

    Args:
        year (int, str): The year as an integer or a string that can be converted to an integer.

    Returns:
        datetime.date: A datetime.date object representing December 31st of the given year.
        None: If the input cannot be converted to an integer or if the input is invalid.
    """
    try:
        year = int(year)
    except (TypeError, ValueError):
        return None

    return datetime.date(year, 12, 31)


def convert_reporting_column(df, column_name, date_conversion_func, date_format):
    """
    Convert the specified column in the DataFrame to a new date format using a given date conversion function.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column to convert.
        column_name (str): The name of the column to convert.
        date_conversion_func (function): The function to apply to each date in the column.
        date_format (str): The new date format to apply to the converted column.
        
    Returns:
        pd.DataFrame: The DataFrame with the specified column converted to the new date format.
    """
    df[column_name] = pd.to_datetime(df[column_name].apply(date_conversion_func))
    df[column_name] = df[column_name].dt.strftime("%d/%m/%Y")
    return df


def filter_by_date_format(df, column_name, date_format_regex):
    """
    Filter the DataFrame by keeping rows where the specified column matches the given date format regex.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column to filter.
        column_name (str): The name of the column to filter.
        date_format_regex (str): The regex pattern representing the date format to filter by.
        
    Returns:
        pd.DataFrame: The DataFrame filtered by the specified date format regex.
    """
    df[column_name] = df[column_name].astype(str)
    date_format_mask = df[column_name].str.match(date_format_regex)
    return df[date_format_mask]


def convert_to_csv(df, file_path):
    """
    Convert a pandas DataFrame to a CSV file and save it to the specified file path.

    Args:
        df (pandas.DataFrame): The DataFrame to be converted and saved as a CSV file.
        file_path (str): The file path where the CSV file should be saved, including the file name.

    Returns:
        None: This function does not return any value. It saves the DataFrame as a CSV file at the specified file path.
    """
    df.to_csv(file_path, index=False)


date_cols = ["DoC issue date", "Reporting Period", "DoC expiry date"]


def convert_and_format_date_columns_to_string(df: pd.DataFrame, date_columns: list = date_cols) -> pd.DataFrame:
    """
    Convert date strings in a DataFrame to the format 'YYYY-MM-DD' and store them as strings.

    :param df: The input DataFrame
    :param date_columns: A list of column names to reformat (default: ['Reporting Period', 'DoC issue date', 'DoC expiry date'])
    :return: The modified DataFrame with date columns reformatted as strings
    """
    if date_columns is None:
        date_columns = ["Reporting Period", "DoC issue date", "DoC expiry date"]

    for col in date_columns:
        if col in df.columns and df[col].dtype == "object":
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d").astype(str)

    return df

