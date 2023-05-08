import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_ship_type_counts(ship_type_counts):
    """
    Plot a bar chart representing the number of ships by ship type.
    
    Args:
        ship_type_counts (pd.Series): A pandas Series containing ship type counts.
    """
    plt.figure(figsize=(8, 7))  # Increase the size of the figure
    ax = ship_type_counts.plot(kind="bar")

    # Decrease font size of count values and ship names
    ax.tick_params(axis="both", labelsize=8)
    plt.xticks(rotation=90)

    # Remove top and right part of the box containing the plot
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Ship Type", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.title("Number of Ships by Type", fontsize=14)
    plt.show()


def plot_emissions_profiles(df):
    """
    Plot a box plot representing the emissions profiles by ship type.
    
    Args:
        df (pd.DataFrame): A pandas DataFrame containing the columns 'Ship type' and 'Total CO₂ emissions [m tonnes]'.
    """
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x="Ship type", y="Total CO₂ emissions [m tonnes]", data=df)

    # Rotate ship type labels to be vertical
    plt.xticks(rotation="vertical")

    # Remove top and right part of the box containing the plot
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.title("Emissions Profiles by Ship Type", fontsize=14)
    plt.xlabel("Ship Type", fontsize=12)
    plt.ylabel("Total CO₂ emissions [m tonnes]", fontsize=12)
    plt.show()


def plot_emissions(annual_emissions):
    """
    Plot a bar chart representing the total CO₂ emissions by year.
    
    Args:
        annual_emissions (pd.DataFrame): A pandas DataFrame containing the columns 'Year' and 'Total CO₂ emissions [m tonnes]'.
    """
    # Set the figure size (width, height) in inches
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the total emissions as a bar plot with reduced bar width
    ax.bar(
        annual_emissions["Year"], annual_emissions["Total CO₂ emissions [m tonnes]"], width=0.5, label="Total Emissions"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Total CO₂ emissions [m tonnes]")
    ax.legend()

    # Set x-axis ticks to integer years
    ax.set_xticks(annual_emissions["Year"])

    # Remove top and right part of the box containing the plot
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.title("Total CO₂ Emissions by Year")
    sns.despine(top=True, right=True)

    plt.show()


def plot_relationship(
    data, correlation, x_col="Total fuel consumption [m tonnes]", y_col="Total CO₂ emissions [m tonnes]"
):
    """
    Plot the relationship between two variables in the given data along with their correlation.
    
    The function creates a scatter plot with a regression line to show the relationship between the two variables.
    It also displays the correlation value in the plot title.
    
    Args:
        data (pd.DataFrame): A pandas DataFrame containing the x_col and y_col columns.
        correlation (float): The correlation value between the x_col and y_col columns.
        x_col (str, optional): The name of the column for the x-axis. Defaults to 'Total fuel consumption [m tonnes]'.
        y_col (str, optional): The name of the column for the y-axis. Defaults to 'Total CO₂ emissions [m tonnes]'.
    """
    # Set the plot style
    sns.set(style="whitegrid")

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x_col, y=y_col, data=data)

    # Customize the plot
    plt.title(f"Relationship between {x_col} and {y_col}\nCorrelation: {correlation:.2f}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)

    # Remove the top and right part of the box
    sns.despine(top=True, right=True)

    # Display the plot
    plt.show()


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
