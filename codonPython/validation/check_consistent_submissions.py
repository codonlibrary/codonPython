import pandas as pd


def check_consistent_submissions(
    data,
    national_geog_level: str = "National",
    geography_col: str = "Org_Level",
    submissions_col: str = "Value_Unsuppressed",
    measure_col: str = "Measure",
) -> bool:
    """
    Check total submissions for each measure are the same across all geography levels
    except national.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame of data to check.
    national_geog_level : str, default = "National"
        Geography level code for national values.
    geography_col : str, default = "Org_Level"
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
    ...   national_geog_level = "N",
    ...   geography_col = "Geog",
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
        not isinstance(submissions_col, str)
        or not isinstance(measure_col, str)
        or not isinstance(geography_col, str)
        or not isinstance(national_geog_level, str)
    ):
        raise ValueError(
            "Please input strings for column names and national geography level."
        )
    if (
        submissions_col not in data.columns
        or measure_col not in data.columns
        or geography_col not in data.columns
    ):
        raise KeyError("Check column names correspond to the DataFrame.")

    # All non-national measures should have only one unique submission number for each
    # geography level.
    submissions_by_measure = (
        data[data[geography_col] != national_geog_level]
        .groupby(measure_col)
        .agg({submissions_col: "nunique"})
    )
    result = (submissions_by_measure[submissions_col] == 1).all()

    return result
