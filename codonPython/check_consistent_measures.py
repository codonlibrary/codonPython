import pandas as pd
import numpy as np


def check_consistent_measures(
    data,
    geography_col: str = "Org_Level",
    measure_col: str = "Measure",
    measures_set: set = set(),
) -> bool:
    """
    Check every measure is in every geography level.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame of data to check.
    geography_col : str, default = "Org_Level"
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
    ...   geography_col = "Geog",
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

    if data.isna().any(axis=None):
        raise ValueError(
            f"Missing values at locations {list(map(tuple, np.argwhere(data.isna().values)))}"
        )
    if not isinstance(geography_col, str) or not isinstance(measure_col, str):
        raise ValueError("Please input strings for column indexes.")
    if not isinstance(measures_set, set):
        raise ValueError("Please input a set object for measures")
    if geography_col not in data.columns or measure_col not in data.columns:
        raise KeyError("Check column names correspond to the DataFrame.")

    # Every geography level should have the same set of measures as the global set.
    global_set = measures_set if measures_set else set(data[measure_col].unique())
    subsets = data.groupby(geography_col).agg({measure_col: "unique"})
    subset_agreement = all(set(x) == global_set for x in subsets[measure_col])

    return subset_agreement
