from codonPython.tolerance import check_tolerance
import numpy as np
import pandas as pd
# import pandas.util.testing as pdt
import pytest


@pytest.mark.parametrize("t, y, to_exclude, poly_features, alpha, forecast, expected", [
    (
        np.array([1234,1235,1236,1237,1238,1239,1240,1241,1242]),
        np.array([1,2,3,4,5,5.5,6,6.5,7]),
        2,
        [1, 2],
        0.05,
        False,
        pd.DataFrame({
            'yhat_u': [
                8.11380197739608,
                9.051653693670929,
                7.127135023632205,
                7.735627110021585,
            ],
            'yobs': [6.5, 7.0, 6.5, 7.0],
            'yhat': [
                7.214285714285714,
                8.071428571428573,
                6.500000000000002,
                6.821428571428574,
            ],
            'yhat_l': [
                6.31476945117535,
                7.091203449186216,
                5.872864976367799,
                5.907230032835563,
            ],
            'polynomial': [1, 1, 2, 2]
        })
    ),
    (
        np.array([1234,1235,1236,1237,1238,1239,1240,1241,1242]),
        np.array([1,2,3,4,5,5.5,6,6.5,7]),
        2,
        [3],
        0.05,
        True,
        pd.DataFrame({
            'yhat_u': [
                6.753927165005773,
                7.214574732953706,
                7.218216279340497,
                7.3980478897523225,
                7.575355558900247,
                7.750571186675458,
                7.924372393971117
            ],
            'yobs': [6.5, 7.0, np.nan, np.nan, np.nan, np.nan, np.nan],
            'yhat': [
                6.0000000000000036,
                5.571428571428576,
                5.5659511039999785,
                5.249235468428623,
                4.842301211809431,
                4.339894601476199,
                3.7367619047620617
            ],
            'yhat_l': [
                5.2460728349942345,
                3.928282409903445,
                3.9136859286594596,
                3.100423047104923,
                2.1092468647186156,
                0.929218016276939,
                -0.45084858444699405
            ],
            'polynomial': [3, 3, 3, 3, 3, 3, 3]
        })
    ),
])
def test_tolerance_checking_BAU(t, y, to_exclude, poly_features, alpha, forecast, expected):
    obtained = check_tolerance(
        t,
        y,
        to_exclude=to_exclude,
        poly_features=poly_features,
        alpha=alpha,
        forecast=forecast,
    )
    assert expected.equals(obtained)


#@pytest.mark.parametrize("t, y, to_exclude, poly_features, alpha, forecast", [])