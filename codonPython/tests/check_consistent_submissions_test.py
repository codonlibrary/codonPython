from codonPython.check_consistent_submissions import check_consistent_submissions
import pandas as pd
import numpy as np
import pytest


@pytest.mark.parametrize(
    "data, national_geog_level, geography_col, submissions_col, measure_col, expected",
    [
        (
            pd.DataFrame(
                {
                    "Geog": ["N", "N", "Region", "Region", "Local", "Local"],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "submissions": [4, 2, 2, 1, 2, 1],
                }
            ),
            "N",
            "Geog",
            "submissions",
            "measure",
            True,
        ),
        (
            pd.DataFrame(
                {
                    "Org_Level": [
                        "National",
                        "National",
                        "Region",
                        "Region",
                        "Local",
                        "Local",
                    ],
                    "Measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "Value_Unsuppressed": [4, 2, 3, 1, 2, 1],
                }
            ),
            "National",
            "Org_Level",
            "Value_Unsuppressed",
            "Measure",
            False,
        ),
    ],
)
def test_each_consistent_measure_BAU(
    data, national_geog_level, geography_col, submissions_col, measure_col, expected
):
    assert expected == check_consistent_submissions(
        data, national_geog_level, geography_col, submissions_col, measure_col
    )


@pytest.mark.parametrize(
    "data, national_geog_level, geography_col, submissions_col, measure_col",
    [
        (
            pd.DataFrame(
                {
                    "Geog": ["N", "N", "Region", "Region", "Local", "Local"],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "submissions": [4, 2, 2, 1, 2, 1],
                }
            ),
            1,
            "Geog",
            "submissions",
            "measure",
        ),
        (
            pd.DataFrame(
                {
                    "Geog": ["N", "N", "Region", "Region", "Local", "Local"],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "submissions": [4, 2, 2, 1, 2, 1],
                }
            ),
            "N",
            False,
            "submissions",
            "measure",
        ),
        (
            pd.DataFrame(
                {
                    "Geog": ["N", "N", "Region", "Region", "Local", "Local"],
                    "measure": ["m1", "m2", "m2", "m2", "m1", "m2"],
                    "submissions": [4, 2, 2, 1, 2, 1],
                }
            ),
            "N",
            "Geog",
            4.2,
            "measure",
        ),
    ],
)
def test_each_consistent_submissions_valueErrors(
    data, national_geog_level, geography_col, submissions_col, measure_col
):
    with pytest.raises(ValueError):
        check_consistent_submissions(
            data, national_geog_level, geography_col, submissions_col, measure_col
        )


@pytest.mark.parametrize(
    "data, national_geog_level, geography_col, submissions_col, measure_col",
    [
        (
            pd.DataFrame(
                {
                    "Geog": ["N", "N", "Region", "Region", "Local", "Local"],
                    "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
                    "submissions": [4, 2, 2, 1, 2, 1],
                }
            ),
            "N",
            "Geog",
            "submissions",
            "measurez",
        )
    ],
)
def test_each_consistent_submissions_colError(
    data, national_geog_level, geography_col, submissions_col, measure_col
):
    with pytest.raises(KeyError):
        check_consistent_submissions(
            data, national_geog_level, geography_col, submissions_col, measure_col
        )
