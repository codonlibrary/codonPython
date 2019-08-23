import numpy
import pandas as pd

def count_null(dataframe: pd.DataFrame) -> bool:
    """
    Checks a pandas dataframe for null values

    This function takes a pandas dataframe supplied as an argument and returns a boolean value representing any null values contained

    Parameters
    ----------
    data : pandas.DataFrame
        Dataframe to be checked for null values

    Returns
    -------
    out : bool
        A True or False response based on if a dataframe contains null values

    Examples
    --------
    >>> count_null(data)
    True
    >>> count_null(data)
    False
    """
    null_count = dataframe.isnull().values.any()
    col_names = dataframe.columns.tolist()
        
    if null_count == True:
        col_value = dataframe.isnull().any().tolist()
        print(col_names)
        print(col_value)
        return True
    else:
        print("No null values found")
        return False