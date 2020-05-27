import datetime
from dateutil.relativedelta import relativedelta

def add_time(date : str, days : int=0, months : int=0, years : int=0) -> str: 
    
    """
    This function takes a date as a string input in the 'yyyy-mm-dd' format and returns 
    transpose of the date, given the specified number of days, months and years. 
    To substract days, months, years from the date passed, use negative values. 
    
    Parameters
    -----------
    date : string 
        Original date
        
    days : int
        Days to add/substract
        default = 0
        
    months : int
        Months to add/substract
        default = 0
        
    years : int
        Years to add/substract
        default = 0
        
    Returns
    -------
    str
    
    Examples
    -------
    >>> add_time('2018-03-04', months=4)
    '2018-07-04'
     
    >>> add_time('2018-03-04', days=-90)
    '2017-12-04'

    >>> add_time('2018-03-04', years=2)
    '2020-03-04'

    """
    
    return str((datetime.datetime.strptime(date,'%Y-%m-%d') + relativedelta(days=int(days), months=int(months), years=int(years))).strftime(('%Y-%m-%d')))
