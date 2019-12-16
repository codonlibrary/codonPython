def suppress_value(valuein: int, rc: str = "*", upper: int = 100000000) -> str:
    """
    Suppress values less than or equal to 7, round all non-national values.

    This function suppresses value if it is less than or equal to 7.
    If value is 0 then it will remain as 0.
    If value is at national level it will remain unsuppressed.
    All other values will be rounded to the nearest 5.

    Parameters
    ----------
    valuein : int
        Metric value
    rc : str
        Replacement character if value needs suppressing
    upper : int
        Upper limit for suppression of numbers

    Returns
    -------
    out : str
        Suppressed value (*), 0 or valuein if greater than 7 or national

    Examples
    --------
    >>> suppress_value(3)
    '*'
    >>> suppress_value(24)
    '25'
    >>> suppress_value(0)
    '0'
    """
    base = 5

    if not isinstance(valuein, int):
        raise ValueError("The input: {} is not an integer.".format(valuein))

    if valuein < 0:
        raise ValueError("The input: {} is less than 0.".format(valuein))
    elif valuein == 0:
        valueout = str(valuein)
    elif valuein >= 1 and valuein <= 7:
        valueout = rc
    elif valuein > 7 and valuein <= upper:
        valueout = str(base * round(valuein / base))
    else:
        raise ValueError("The input: {} is greater than: {}.".format(valuein, upper))
    return valueout
