from codonPython.output_checker import (
    check_null,
    check_nat_val,
    check_consistent_submissions,
    check_consistent_measures,
)
import numpy as np
import pandas as pd
import pytest


# Null check tests
testdata = pd.DataFrame({
    "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "col2": [11, 12, 13, 14, 15, np.nan, np.nan, 18, 19, 20],
})


@pytest.mark.parametrize("df, columns_to_be_checked, expected", [
    (testdata.iloc[:5, :], ["col1", "col2"], 0),
    (testdata, ["col2"], 2),
])
def test_nullcheck_BAU(df, columns_to_be_checked, expected):
    assert check_null(df, columns_to_be_checked) == expected


@pytest.mark.parametrize("df, columns_to_be_checked", [
    (testdata, 0.01),
])
def test_nullcheck_ValueError(df, columns_to_be_checked):
    with pytest.raises(ValueError):
        check_null(df, columns_to_be_checked)


@pytest.mark.parametrize("df, columns_to_be_checked", [
    (testdata, ["wrong_column"]),
])
def test_nullcheck_KeyError(df, columns_to_be_checked):
    with pytest.raises(KeyError):
        check_null(df, columns_to_be_checked)


# National value tests
df = pd.DataFrame({
    "Breakdown": [
        'National', 'CCG', 'CCG', 'Provider', 'Provider',
        'National', 'CCG', 'CCG', 'Provider', 'Provider',
        'National', 'CCG', 'CCG', 'Provider', 'Provider',
    ],
    "measure": [
        'm1', 'm1', 'm1', 'm1', 'm1',
        'm2', 'm2', 'm2', 'm2', 'm2',
        'm3', 'm3', 'm3', 'm3', 'm3',
    ],
    "Value_Unsuppressed": [
        9, 4, 5, 3, 6,
        11, 2, 9, 7, 4,
        9, 5, 4, 6, 3
    ],
})


@pytest.mark.parametrize("df, breakdown_col, measure_col, value_col, nat_val, expected", [
    (
        df,
        "Breakdown",
        "measure",
        "Value_Unsuppressed",
        "National",
        True
    ),
])
def test_natval_BAU(df, breakdown_col, measure_col, value_col, nat_val, expected):
    assert check_nat_val(
        df,
        breakdown_col=breakdown_col,
        measure_col=measure_col,
        value_col=value_col,
        nat_val=nat_val,
    ) == expected


@pytest.mark.parametrize("df, breakdown_col, measure_col, value_col, nat_val", [
    (
        df,
        "Breakdown",
        23,  # Not a string
        "Value_Unsuppressed",
        "National",
    ),
    (
        df,
        0.1,  # Not a string
        "Measure",
        "Value_Unsuppressed",
        "National",
    ),
    (
        df,
        "Breakdown",
        "Measure",
        pd.DataFrame({"wrong": [1, 2, 3]}),  # Not a string
        "National",
    ),
    (
        df,
        "Breakdown",
        "Measure",
        "Value_Unsuppressed",
        set({"m1", "m2"}),  # Not a string
    ),
])
def test_natval_ValueErrors(df, breakdown_col, measure_col, value_col, nat_val):
    with pytest.raises(ValueError):
        check_nat_val(
            df,
            breakdown_col=breakdown_col,
            measure_col=measure_col,
            value_col=value_col,
            nat_val=nat_val,
        )


@pytest.mark.parametrize("df, breakdown_col, measure_col, value_col, nat_val", [
    (
        df,
        "Breakdown",
        "measure",
        "Wrong_Column",
        "National",
    )
])
def test_natval_KeyErrors(df, breakdown_col, measure_col, value_col, nat_val):
    with pytest.raises(KeyError):
        check_nat_val(
            df,
            breakdown_col=breakdown_col,
            measure_col=measure_col,
            value_col=value_col,
            nat_val=nat_val,
        )


# Check consistent measures tests
@pytest.mark.parametrize("df, breakdown_col, measure_col, measures_set, expected", [
    (
        pd.DataFrame({
            "Geog": ["National", "National", "Region", "Region", "Local", "Local"],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
            "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
        }),
        "Geog",
        "measure",
        set({"m1", "m2"}),
        True
    ),
    (
        pd.DataFrame({
            "Geog": ["National", "National", "Region", "Region", "Local", "Local"],
            "measure": ["m1", "m2", "m1", "m3", "m1", "m2"],
            "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
        }),
        "Geog",
        "measure",
        set({"m1", "m2"}),
        False
    )
])
def test_each_org_levels_BAU(df, breakdown_col, measure_col, measures_set, expected):
    assert expected == check_consistent_measures(
        df, breakdown_col, measure_col, measures_set)


@pytest.mark.parametrize("df, breakdown_col, measure_col, measures_set", [
    (
        pd.DataFrame({
            "Geog": ["National", "National", "Region", "Region", "Local", "Local"],
            "measure": ["m1", "m2", "m1", np.nan, "m1", "m2"],
            "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
        }),
        "Geog",
        "measure",
        set({"m1", "m2"}),
    ),
])
def test_each_org_levels_valueErrors_measure_col(df, breakdown_col, measure_col, measures_set):
    with pytest.raises(ValueError):
        check_consistent_measures(df, breakdown_col, measure_col, measures_set)


@pytest.mark.parametrize("df, breakdown_col, measure_col, measures_set", [
    (
        pd.DataFrame({
            "Geog": ["National", "National", "Region", "Region", "Local", "Local"],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2"],
            "Value_Unsuppressed": [4, 2, 2, 1, 2, 1],
        }),
        "Global",
        "measure",
        set({"m1", "m2"}),
    )
])
def test_each_breakdown_col_keyError(df, breakdown_col, measure_col, measures_set):
    with pytest.raises(KeyError):
        check_consistent_measures(df, breakdown_col, measure_col, measures_set)


@pytest.mark.parametrize("df, nat_val, breakdown_col, submissions_col, measure_col, expected", [
    (
        pd.DataFrame({
            "Geog": ["N", "N", "Region", "Region", "Local", "Local", ],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2", ],
            "submissions": [4, 2, 2, 1, 2, 1, ],
        }),
        "N",
        "Geog",
        "submissions",
        "measure",
        True
    ),
    (
        pd.DataFrame({
            "Org_Level": ["National", "National", "Region", "Region", "Local", "Local", ],
            "Measure": ["m1", "m2", "m1", "m2", "m1", "m2", ],
            "Value_Unsuppressed": [4, 2, 3, 1, 2, 1, ],
        }),
        "National",
        "Org_Level",
        "Value_Unsuppressed",
        "Measure",
        False
    )
])
def test_each_consistent_measure_BAU(df, nat_val, breakdown_col, submissions_col, measure_col, expected):
    assert expected == check_consistent_submissions(
        df, nat_val, breakdown_col, submissions_col, measure_col)


@pytest.mark.parametrize("df, nat_val, breakdown_col, submissions_col, measure_col", [
    (
        pd.DataFrame({
            "Geog": ["N", "N", "Region", "Region", "Local", "Local", ],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2", ],
            "submissions": [4, 2, 2, 1, 2, 1, ],
        }),
        1,
        "Geog",
        "submissions",
        "measure"
    ),
    (
        pd.DataFrame({
            "Geog": ["N", "N", "Region", "Region", "Local", "Local", ],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2", ],
            "submissions": [4, 2, 2, 1, 2, 1, ],
        }),
        "N",
        False,
        "submissions",
        "measure"
    ),
    (
        pd.DataFrame({
            "Geog": ["N", "N", "Region", "Region", "Local", "Local", ],
            "measure": ["m1", "m2", "m2", "m2", "m1", "m2", ],
            "submissions": [4, 2, 2, 1, 2, 1, ],
        }),
        "N",
        "Geog",
        4.2,
        "measure"
    )
])
def test_each_consistent_submissions_valueErrors(df, nat_val, breakdown_col, submissions_col, measure_col):
    with pytest.raises(ValueError):
        check_consistent_submissions(
            df, nat_val, breakdown_col, submissions_col, measure_col)


@pytest.mark.parametrize("df, nat_val, breakdown_col, submissions_col, measure_col", [
    (
        pd.DataFrame({
            "Geog": ["N", "N", "Region", "Region", "Local", "Local", ],
            "measure": ["m1", "m2", "m1", "m2", "m1", "m2", ],
            "submissions": [4, 2, 2, 1, 2, 1, ],
        }),
        "N",
        "Geog",
        "submissions",
        "measurez"
    )
])
def test_each_consistent_submissions_colError(df, nat_val, breakdown_col, submissions_col, measure_col):
    with pytest.raises(KeyError):
        check_consistent_submissions(
            df, nat_val, breakdown_col, submissions_col, measure_col)


#TODO write tests for wrapper
