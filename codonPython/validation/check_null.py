import numpy
import pandas as pd


def check_null(dataframe: pd.DataFrame, columns_to_be_checked: list) -> int:
    """
    Checks a pandas dataframe for null values

    This function takes a pandas dataframe supplied as an argument and returns a integer value
    representing any null values found within the columns to check.

    Parameters
    ----------
    data : pandas.DataFrame
        Dataframe to read
    columns_to_be_checked: list
        Given dataframe columns to be checked for null values

    Returns
    -------
    out : int
        The number of null values found in the given columns

    Examples
    --------
    >>> check_null(dataframe = pd.DataFrame({'col1': [1,2], 'col2': [3,4]}),columns_to_be_checked = ['col1', 'col2'])
    0
    >>> check_null(dataframe = pd.DataFrame({'col1': [1,numpy.nan], 'col2': [3,4]}),columns_to_be_checked = ['col1'])
    1
    """

    if not isinstance(columns_to_be_checked, list):
        raise ValueError("Please make sure that all your columns passed are strings")

    for eachCol in columns_to_be_checked:
        if eachCol not in dataframe.columns:
            raise KeyError(
                "Please check the column names correspond to values in the DataFrame."
            )

    null_count = 0
    for eachColumn in columns_to_be_checked:
        prev_null_count = null_count
        null_count = prev_null_count + (len(dataframe) - dataframe[eachColumn].count())

    return null_count
