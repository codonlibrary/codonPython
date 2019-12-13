from codonPython.check_null import check_null
import numpy as np
import pandas as pd
import pytest

testdata = pd.DataFrame(
    {
        "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "col2": [11, 12, 13, 14, 15, np.nan, np.nan, 18, 19, 20],
    }
)


@pytest.mark.parametrize(
    "dataframe, columns_to_be_checked, expected",
    [(testdata.iloc[:5, :], ["col1", "col2"], 0), (testdata, ["col2"], 2)],
)
def test_BAU(dataframe, columns_to_be_checked, expected):
    assert check_null(dataframe, columns_to_be_checked) == expected


@pytest.mark.parametrize("dataframe, columns_to_be_checked", [(testdata, 0.01)])
def test_ValueError(dataframe, columns_to_be_checked):
    with pytest.raises(ValueError):
        check_null(dataframe, columns_to_be_checked)


@pytest.mark.parametrize(
    "dataframe, columns_to_be_checked", [(testdata, ["wrong_column"])]
)
def test_KeyError(dataframe, columns_to_be_checked):
    with pytest.raises(KeyError):
        check_null(dataframe, columns_to_be_checked)
