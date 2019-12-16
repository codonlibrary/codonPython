from codonPython.check_consistent_measures import check_consistent_measures
import pandas as pd
import numpy as np
import pytest


@pytest.mark.parametrize(
    "data, geography_col, measure_col, measures_set, expected",
    [
        (
            pd.DataFrame(
                {
                    "Geog": [
                        "National",
                        "National",
                        "Region",
                        "Region",
                        "Local",
                        "Local",
                    ],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
                }
            ),
            "Geog",
            "measure",
            set({"m1", "m2"}),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "Geog": [
                        "National",
                        "National",
                        "Region",
                        "Region",
                        "Local",
                        "Local",
                    ],
                    "measure": ["m1", "m2", "m1", "m3", "m1", "m2"],
                    "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
                }
            ),
            "Geog",
            "measure",
            set({"m1", "m2"}),
            False,
        ),
    ],
)
def test_each_org_levels_BAU(data, geography_col, measure_col, measures_set, expected):
    assert expected == check_consistent_measures(
        data, geography_col, measure_col, measures_set
    )


@pytest.mark.parametrize(
    "data, geography_col, measure_col, measures_set",
    [
        (
            pd.DataFrame(
                {
                    "Geog": [
                        "National",
                        "National",
                        "Region",
                        "Region",
                        "Local",
                        "Local",
                    ],
                    "measure": ["m1", "m2", "m1", np.nan, "m1", "m2"],
                    "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
                }
            ),
            "Geog",
            "measure",
            set({"m1", "m2"}),
        )
    ],
)
def test_each_org_levels_valueErrors_measure_col(
    data, geography_col, measure_col, measures_set
):
    with pytest.raises(ValueError):
        check_consistent_measures(data, geography_col, measure_col, measures_set)


@pytest.mark.parametrize(
    "data, geography_col, measure_col, measures_set",
    [
        (
            pd.DataFrame(
                {
                    "Geog": [
                        "National",
                        "National",
                        "Region",
                        "Region",
                        "Local",
                        "Local",
                    ],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
                }
            ),
            "Global",
            "measure",
            set({"m1", "m2"}),
        )
    ],
)
def test_each_geography_col_keyError(data, geography_col, measure_col, measures_set):
    with pytest.raises(KeyError):
        check_consistent_measures(data, geography_col, measure_col, measures_set)
