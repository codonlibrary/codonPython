def round_value(valuein: int, base = 5)->int:
    """
    Round values to nearest 5

    This function will round metric values to the nearest 5.
    
    Parameters
    ----------
    valuein : int
        Metric value
    base :
        number which we are rounding to i.e. to the nearest 5
    
    Returns
    ----------
    out : int
        Rounded value 
    
    Examples
    ----------
    >>> round_value(8)
    '10'
    >>> round_value(20)
    '20'
    >>> round_value(46)
    '45'
    """

    return base * round(valuein/base)

def suppress_value(valuein: int, rc:str = '*')->str:
    """
    Suppress values less than or equal to 7

    This function takes the metric value and suppresses it if it is less than or equal to 7. 
    If the metric value is 0 then it will remain as 0.

    Parameters
    ----------
    valuein : int
        Metric value
    rc : str
        Replacement character if value needs suppressing

    Returns
    -------
    out : str
        Suppressed value (*), 0 or valuein if greater than 7

    Examples
    --------
    >>> suppress_value(3)
    '*'
    >>> suppress_value(24)
    '24'
    >>> suppress_value(0)
    '0'
    """

    if valuein == 0:
        valueout = str(valuein)
    if 1 <= valuein <= 7:
        valueout = rc
    if valuein > 7:
        valueout = str(valuein)
    return valueout
  
