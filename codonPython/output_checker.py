import pandas as pd
import numpy as np


def check_null(df: pd.DataFrame, columns_to_be_checked: list) -> bool:
    """
    Checks a pandas dataframe for null values

    This function takes a pandas dataframe supplied as an argument and returns a integer value representing any null values found within the columns to check

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to read
    columns_to_be_checked: list
        Given dataframe columns to be checked for null values

    Returns
    -------
    out : int
        The number of null values found in the given columns

    Examples
    --------
    >>> check_null(df = pd.DataFrame({'col1': [1,2], 'col2': [3,4]}), columns_to_be_checked = ['col1', 'col2'])
    0
    >>> check_null(df = pd.DataFrame({'col1': [1,np.nan], 'col2': [3,4]}), columns_to_be_checked = ['col1'])
    1
    """

    if not isinstance(columns_to_be_checked, list):
        raise ValueError("Please make sure that all your columns passed are strings")
    else:
        pass

    for eachCol in columns_to_be_checked:
        if eachCol not in df.columns:
            raise KeyError("Please check the column names correspond to values in the DataFrame.")
        else:
            pass

    null_count = 0
    for eachColumn in columns_to_be_checked:
        prev_null_count = null_count
        null_count = prev_null_count + (len(df) - df[eachColumn].count())

    return null_count


def check_nat_val(
    df: pd.DataFrame,
    breakdown_col: str = "Breakdown",
    measure_col: str = "Measure",
    value_col: str = "Value_Unsuppressed",
    nat_val: str = "National"
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
    ...         'National' ,'CCG', 'CCG', 'Provider', 'Provider','National' ,'CCG', 'CCG',
    ...         'Provider', 'Provider',],
    ...     "Measure" : ['m1', 'm1', 'm1', 'm1', 'm1', 'm2', 'm2', 'm2', 'm2',
    ...         'm2', 'm3', 'm3', 'm3', 'm3', 'm3',],
    ...     "Value_Unsuppressed" : [18, 4, 5, 3, 6, 11, 2, 9, 7, 4, 9, 5, 4, 6, 3],
    ...   }),
    ...   breakdown_col = "Breakdown",
    ...   measure_col = "Measure",
    ...   value_col = "Value_Unsuppressed",
    ...   nat_val = "National",
    ... )
    False
    """

    if not isinstance(breakdown_col, str) or not isinstance(measure_col, str)\
            or not isinstance(value_col, str):
        raise ValueError("Please input strings for column indexes.")
    if not isinstance(nat_val, str):
        raise ValueError("Please input strings for value indexes.")
    if breakdown_col not in df.columns or measure_col not in df.columns or\
            value_col not in df.columns:
        raise KeyError("Check column names correspond to the DataFrame.")
    # aggregate values by measure and breakdown
    grouped = df.groupby([measure_col, breakdown_col]).agg({value_col: sum})\
        .reset_index()
    national = grouped.loc[grouped[breakdown_col] == nat_val].reset_index()
    non_national = grouped.loc[grouped[breakdown_col] != nat_val].reset_index()
    # check values are less than or equal to national value for each measure
    join = pd.merge(non_national, national, left_on=measure_col,
                    right_on=measure_col, how='left')
    left = value_col + '_x'
    right = value_col + '_y'
    join['Check'] = join[right] <= join[left]
    result = all(join['Check'])
    return result


def check_consistent_measures(
    df: pd.DataFrame,
    breakdown_col: str = "Org_Level",
    measure_col: str = "Measure",
    measures_set: set = set(),
    ) -> bool:
    """
    Check every measure is in every geography level.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of data to check.
    breakdown_col : str, default = "Org_Level"
        Column name for the geography level.
    measure_col : str, default = "Measure"
        Column name for measure
    measures_set : set, default = set()
        Set of measures that should be in every geography level. If empty, the existing
        global set is presumed to be correct.

    Returns
    -------
    bool
        Whether the checks have been passed.

    Examples
    --------
    >>> check_consistent_measures(
    ...   pd.DataFrame({
    ...     "Geog" : ["National" ,"National", "Region", "Region", "Local", "Local",],
    ...     "measure" : ["m1", "m2", "m1", "m2", "m1", "m2",],
    ...     "Value_Unsuppressed" : [4, 2, 2, 1, 2, 1,],
    ...   }),
    ...   breakdown_col = "Geog",
    ...   measure_col = "measure",
    ...   measures_set = set({"m1", "m2"}),
    ... )
    True
    >>> check_consistent_measures(
    ...   pd.DataFrame({
    ...     "Org_Level" : ["National" ,"National", "Region", "Region", "Local", "Local",],
    ...     "Measure" : ["m1", "m3", "m1", "m2", "m1", "m2",],
    ...     "Value_Unsuppressed" : [4, 2, 2, 1, 2, 1,],
    ...   })
    ... )
    False
    """

    if df.isna().any(axis=None):
        raise ValueError(
        f"Missing values at locations {list(map(tuple, np.argwhere(df.isna().values)))}"
        )
    if not isinstance(breakdown_col, str) or not isinstance(measure_col, str):
        raise ValueError("Please input strings for column indexes.")
    if not isinstance(measures_set, set):
        raise ValueError("Please input a set object for measures")
    if breakdown_col not in df.columns or measure_col not in df.columns:
        raise KeyError("Check column names correspond to the DataFrame.")

    # Every geography level should have the same set of measures as the global set.
    global_set = measures_set if measures_set else set(df[measure_col].unique())
    subsets = df.groupby(breakdown_col) \
                    .agg({measure_col: "unique"})
    subset_agreement = all(set(x) == global_set for x in subsets[measure_col])

    return subset_agreement


def check_consistent_submissions(
    df: pd.DataFrame,
    nat_val: str = "National",
    breakdown_col: str = "Org_Level",
    submissions_col: str = "Value_Unsuppressed",
    measure_col: str = "Measure", 
    ) -> bool:
    """
    Check total submissions for each measure are the same across all geography levels
    except national.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of data to check.
    nat_val : str, default = "National"
        Geography level code for national values.
    breakdown_col : str, default = "Org_Level"
        Column name for the geography level.
    submissions_col : str, default = "Value_Unsuppressed"
        Column name for the submissions count.
    measure_col : str, default = "Measure"
        Column name for measure.

    Returns
    -------
    bool
        Whether the checks have been passed.

    Examples
    --------
    >>> check_consistent_submissions(
    ...   pd.DataFrame({
    ...     "Geog" : ["N" ,"N", "Region", "Region", "Local", "Local",],
    ...     "measure" : ["m1", "m2", "m1", "m2", "m1", "m2",],
    ...     "submissions" : [4, 2, 2, 1, 2, 1,],
    ...   }),
    ...   nat_val = "N",
    ...   breakdown_col = "Geog",
    ...   submissions_col = "submissions",
    ...   measure_col = "measure",
    ... )
    True
    >>> check_consistent_submissions(
    ...   pd.DataFrame({
    ...     "Org_Level" : ["National" ,"National", "Region", "Region", "Local", "Local",],
    ...     "Measure" : ["m1", "m2", "m1", "m2", "m1", "m2",],
    ...     "Value_Unsuppressed" : [4, 2, 3, 1, 2, 1,],
    ...   })
    ... )
    False
    """

    if (
        not isinstance(submissions_col, str) or
        not isinstance(measure_col, str) or
        not isinstance(breakdown_col, str) or
        not isinstance(nat_val, str)
    ):
        raise ValueError("Please input strings for column names and national geography level.")
    if (
        submissions_col not in df.columns or
        measure_col not in df.columns or
        breakdown_col not in df.columns
    ):
        raise KeyError("Check column names correspond to the DataFrame.")

    # All non-national measures should have only one unique submission number for each
    # geography level.
    submissions_by_measure = df[df[breakdown_col] != nat_val] \
                                .groupby(measure_col) \
                                    .agg({submissions_col: "nunique"})
    result = (submissions_by_measure[submissions_col] == 1).all()

    return result


def output_checker(
    df: pd.DataFrame,
    columns_to_be_checked: list,
    nat_val: str = "National",
    breakdown_col: str = "Breakdown",
    value_col: str = "Value_Unsuppressed",
    measure_col: str = "Measure",
    measures_set: set = set()
    ) -> bool:
    """
    Wrapper to call each of the output checking functions for national figures.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of data to check.
    columns_to_be_checked: list
        Given dataframe columns to be checked for null values
    nat_val : str, default = "National"
        Geography level code for national values.
    breakdown_col : str, default = "Breakdown"
        Column name for the breakdown level.
    value_col : str, default = "Value_Unsuppressed"
        Column name for values
    measure_col : str, default = "Measure"
        Column name for measures
    measures_set : set, default = set()
        Set of measures that should be in every geography level. If empty, the existing
        global set is presumed to be correct.

    Returns
    ----------
    True
        When the checks have been passed.

    Examples
    ----------
    >>> output_checker(
    ...    pd.DataFrame({
    ...        "Breakdown" : ['National', 'CCG', 'CCG', 'Provider', 'Provider',
    ...                       'National' ,'CCG', 'CCG', 'Provider', 'Provider',
    ...                       'National' ,'CCG', 'CCG', 'Provider', 'Provider',],
    ...        "Measure" : ['m1', 'm1', 'm1', 'm1', 'm1',
    ...                     'm2', 'm2', 'm2', 'm2', 'm2',
    ...                     'm3', 'm3', 'm3', 'm3', 'm3',],
    ...        "Value_Unsuppressed" : [20, 10, 10, 10, 10, 8, 4, 4, 4, 4, 12, 6, 6, 6, 6]
    ...    }),
    ...    columns_to_be_checked = ["Breakdown", "Measure", "Value_Unsuppressed"],
    ...    nat_val = "National",
    ...    breakdown_col = "Breakdown",
    ...    measure_col = "Measure",
    ...    measures_set = set({"m1", "m2", "m3"}),
    ... )
    True
    """
    assert (check_null(df=df, columns_to_be_checked=columns_to_be_checked) == 0), (
        f"Null fields detected at {list(map(tuple, np.argwhere(df.isna().values)))}"
    )
    assert check_nat_val(
        df=df,
        breakdown_col=breakdown_col,
        measure_col=measure_col,
        value_col=value_col,
        nat_val=nat_val,
    ), (
        "The national value is more than the sum of breakdowns for one or more measures."
    )
    assert check_consistent_measures(
        df=df,
        breakdown_col=breakdown_col,
        measure_col=measure_col,
        measures_set=measures_set,
    ), (
        "Measures are inconsistent across breakdowns/geography levels."
    )
    assert check_consistent_submissions(
        df=df,
        nat_val=nat_val,
        breakdown_col=breakdown_col,
        submissions_col=value_col,
        measure_col=measure_col, 
    ), (
        "Submissions are inconsistent for measures across different geography levels"
    )
    return True