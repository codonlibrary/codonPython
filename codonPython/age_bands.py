import math


def age_band_5_years(age: int)->str:
    """
    Place age into appropriate 5 year band

    This function takes the age supplied as an argument and returns a string 
    representing the relevant 5 year banding.

    Parameters
    ----------
    age : int
        Age of the person

    Returns
    -------
    out : str
        The 5 year age band

    Examples
    --------
    >>> age_band_5_years(3)
    '0-4'
    >>> age_band_5_years(-1)
    'Age not known'
    >>> age_band_5_years(95)
    '90 and over'
    """

    if age is None or age < 0:
        return 'Age not known'

    if age > 89:
        if age <  150:
            return '90 and over'
        else:
            raise ValueError 

    lowerbound = 5 * int(math.floor(age / 5))
    upperbound = lowerbound + 4
    return '{}-{}'.format(lowerbound, upperbound)


def age_band_10_years(age: int)->str:
    """
    Place age into appropriate 10 year band

    This function takes the age supplied as an argument and returns a string 
    representing the relevant 10 year banding.

    Parameters
    ----------
    age : int
        Age of the person

    Returns
    -------
    out : str
        The 10 year age band

    Examples
    --------
    >>> age_band_10_years(3)
    '0-9'
    >>> age_band_10_years(-1)
    'Age not known'
    >>> age_band_10_years(95)
    '90 and over'
    """

    if age is None or age < 0:
        return 'Age not known'

    if age > 89:
        if age <  150:
            return '90 and over'
        else:
            raise ValueError 

    lowerbound = 10 * int(math.floor(age / 10))
    upperbound = lowerbound + 9
    return '{}-{}'.format(lowerbound, upperbound)
