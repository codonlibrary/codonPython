import numpy
import pandas as pd

def check_null(dataframe: pd.DataFrame) -> bool:
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
    >>> check_null(data = pd.DataFrame(data = {'col1': [1,2], 'col2': [3,4]}))
    False
    >>> check_null(data = pd.DataFrame({'col1': [1,numpy.nan], 'col2': [3,4]}))
    True
    """
    null_count = dataframe.isnull().values.any()
        
    return null_count