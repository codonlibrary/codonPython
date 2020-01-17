from codonPython.check_nat_val import check_nat_val
import pytest
import pandas as pd


df = pd.DataFrame(
    {
        "Breakdown": [
            "National",
            "CCG",
            "CCG",
            "Provider",
            "Provider",
            "National",
            "CCG",
            "CCG",
            "Provider",
            "Provider",
            "National",
            "CCG",
            "CCG",
            "Provider",
            "Provider",
        ],
        "measure": [
            "m1",
            "m1",
            "m1",
            "m1",
            "m1",
            "m2",
            "m2",
            "m2",
            "m2",
            "m2",
            "m3",
            "m3",
            "m3",
            "m3",
            "m3",
        ],
        "Value_Unsuppressed": [9, 4, 5, 3, 6, 11, 2, 9, 7, 4, 9, 5, 4, 6, 3],
    }
)


@pytest.mark.parametrize(
    "df, breakdown_col, measure_col, value_col, nat_val, expected",
    [(df, "Breakdown", "measure", "Value_Unsuppressed", "National", True)],
)
def test_BAU(df, breakdown_col, measure_col, value_col, nat_val, expected):
    assert (
        check_nat_val(
            df,
            breakdown_col=breakdown_col,
            measure_col=measure_col,
            value_col=value_col,
            nat_val=nat_val,
        )
        == expected
    )


@pytest.mark.parametrize(
    "df, breakdown_col, measure_col, value_col, nat_val",
    [
        (df, "Breakdown", 23, "Value_Unsuppressed", "National"),  # Not a string
        (df, 0.1, "Measure", "Value_Unsuppressed", "National"),  # Not a string
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
    ],
)
def test_ValueErrors(df, breakdown_col, measure_col, value_col, nat_val):
    with pytest.raises(ValueError):
        check_nat_val(
            df,
            breakdown_col=breakdown_col,
            measure_col=measure_col,
            value_col=value_col,
            nat_val=nat_val,
        )


@pytest.mark.parametrize(
    "df, breakdown_col, measure_col, value_col, nat_val",
    [(df, "Breakdown", "measure", "Wrong_Column", "National")],
)
def test_KeyErrors(df, breakdown_col, measure_col, value_col, nat_val):
    with pytest.raises(KeyError):
        check_nat_val(
            df,
            breakdown_col=breakdown_col,
            measure_col=measure_col,
            value_col=value_col,
            nat_val=nat_val,
        )
