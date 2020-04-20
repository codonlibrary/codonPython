import pandas as pd


def check_nat_val(
    df: pd.DataFrame,
    breakdown_col: str = "Breakdown",
    measure_col: str = "Measure",
    value_col: str = "Value_Unsuppressed",
    nat_val: str = "National",
) -> bool:
    """
    Check national value less than or equal to sum of breakdowns.

    This function checks that the national value is less than or equal to the
    sum of each organisation level breakdown.
    This function does not apply to values which are averages.
    This function does not apply to values which are percentages calculated
    from the numerator and denominator.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of data to check.
    breakdown_col : str, default = "Breakdown"
        Column name for the breakdown level.
    measure_col : str, default = "Measure"
        Column name for measures
    value_col : str, default = "Value_Unsuppressed"
        Column name for values
    nat_val : str, default = "National"
        Value in breakdown column denoting national values
    Returns
    -------
    bool
        Whether the checks have been passed.

    Examples
    --------
    >>> check_nat_val(
    ...   df = pd.DataFrame({
    ...     "Breakdown" : ['National', 'CCG', 'CCG', 'Provider', 'Provider',
    ... 'National' ,'CCG', 'CCG', 'Provider', 'Provider','National' ,'CCG', 'CCG',
    ... 'Provider', 'Provider',],
    ...     "Measure" : ['m1', 'm1', 'm1', 'm1', 'm1', 'm2', 'm2', 'm2', 'm2',
    ... 'm2', 'm3', 'm3', 'm3', 'm3', 'm3',],
    ...     "Value_Unsuppressed" : [9, 4, 5, 3, 6, 11, 2, 9, 7, 4, 9, 5, 4, 6,
    ... 3],
    ...   }),
    ...   breakdown_col = "Breakdown",
    ...   measure_col = "Measure",
    ...   value_col = "Value_Unsuppressed",
    ...   nat_val = "National",
    ... )
    True
    >>> check_nat_val(
    ...   df = pd.DataFrame({
    ...     "Breakdown" : ['National', 'CCG', 'CCG', 'Provider', 'Provider',
    ... 'National' ,'CCG', 'CCG', 'Provider', 'Provider','National' ,'CCG', 'CCG',
    ... 'Provider', 'Provider',],
    ...     "Measure" : ['m1', 'm1', 'm1', 'm1', 'm1', 'm2', 'm2', 'm2', 'm2',
    ... 'm2', 'm3', 'm3', 'm3', 'm3', 'm3',],
    ...     "Value_Unsuppressed" : [18, 4, 5, 3, 6, 11, 2, 9, 7, 4, 9, 5, 4, 6,
    ... 3],
    ...   }),
    ...   breakdown_col = "Breakdown",
    ...   measure_col = "Measure",
    ...   value_col = "Value_Unsuppressed",
    ...   nat_val = "National",
    ... )
    False
    """

    if (
        not isinstance(breakdown_col, str)
        or not isinstance(measure_col, str)
        or not isinstance(value_col, str)
    ):
        raise ValueError("Please input strings for column indexes.")
    if not isinstance(nat_val, str):
        raise ValueError("Please input strings for value indexes.")
    if (
        breakdown_col not in df.columns
        or measure_col not in df.columns
        or value_col not in df.columns
    ):
        raise KeyError("Check column names correspond to the DataFrame.")
    # aggregate values by measure and breakdown
    grouped = (
        df.groupby([measure_col, breakdown_col]).agg({value_col: sum}).reset_index()
    )
    national = grouped.loc[grouped[breakdown_col] == nat_val].reset_index()
    non_national = grouped.loc[grouped[breakdown_col] != nat_val].reset_index()
    # check values are less than or equal to national value for each measure
    join = pd.merge(
        non_national, national, left_on=measure_col, right_on=measure_col, how="left"
    )
    left = value_col + "_x"
    right = value_col + "_y"
    join["Check"] = join[right] <= join[left]
    result = all(join["Check"])
    return result
