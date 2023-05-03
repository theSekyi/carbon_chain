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


def calculate_correlation(data, method="pearson"):
    """
    Calculate the correlation coefficient between 'Total fuel consumption [m tonnes]'
    and 'Total CO₂ emissions [m tonnes]' columns in the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame containing the columns.
        method (str, optional): The correlation method. Defaults to 'pearson'.

    Returns:
        float: The correlation coefficient.
    """
    column1 = "Total fuel consumption [m tonnes]"
    column2 = "Total CO₂ emissions [m tonnes]"
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


def plot_bar_plot(df, x_col, y_col):
    """
    Plot a bar plot of the specified columns in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the columns.
        x_col (str): The name of the column for the x-axis.
        y_col (str): The name of the column for the y-axis.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_col, y=y_col, data=df, errorbar=None)
    plt.xticks(rotation="vertical")

    plt.title(f"Mean Technical Efficiency Value by {x_col} (Bar Plot)")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    sns.despine(top=True, right=True)
    plt.show()
