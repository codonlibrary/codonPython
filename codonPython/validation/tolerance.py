import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


def check_tolerance(
    t,
    y,
    to_exclude: int = 1,
    poly_features: list = [1, 2],
    alpha: float = 0.05,
    parse_dates: bool = False,
    predict_all: bool = False,
) -> pd.DataFrame:
    """
    Check that some future values are within a weighted least squares confidence interval.

    Parameters
    ----------
    t : pd.Series
        N explanatory time points of shape (N, 1).
    y : pd.Series
        The corresponding response variable values to X, of shape (N, 1).
    to_exclude : int, default = 1
        How many of the last y values will have their tolerances checked.
    poly_features : list, default = [1, 2]
        List of degrees of polynomial basis to fit to the data. One model will be
        produced for each number in the list, eg. the default will fit a linear and
        a second degree polynomial to the data and return both sets of results.
    alpha : float, default = 0.05
        Alpha parameter for the weighted least squares confidence interval.
    parse_dates : bool, default = True
        Set to true to parse string dates in t
    predict_all : bool, default = False
        Set to true to show predictions for all points of the dataset.


    Returns
    -------
    pd.DataFrame
        DataFrame containing:
            "t"         : Value for t
            "yhat_u"    : Upper condfidence interval for y
            "yobs"      : Observed value for y
            "yhat"      : Predicted value for y
            "yhat_l"    : Lower confidence interval for y
            "polynomial": Max polynomial of model fit to the data


    Examples
    --------
    >>> check_tolerance(
    ...     t = pd.Series([1001,1002,1003,1004,1005,1006]),
    ...     y = pd.Series([2,3,4,4.5,5,5.1]),
    ...     to_exclude = 2,
    ... )
          t     yhat_u  yobs   yhat    yhat_l  polynomial
    0  1005   6.817413   5.0  5.500  4.182587           1
    1  1006   7.952702   5.1  6.350  4.747298           1
    2  1005   9.077182   5.0  4.875  0.672818           2
    3  1006  13.252339   5.1  4.975 -3.302339           2
    """

    if not isinstance(poly_features, list):
        raise ValueError(
            "Please input a list of integers from 0 to 4 for poly_features."
        )
    assert all(
        0 <= degree <= 4 for degree in poly_features
    ), "Please ensure all numbers in poly_features are from 0 to 4."
    if not isinstance(alpha, float) or 0 > alpha >= 1:
        raise ValueError("Please input a float between 0 and 1 for alpha.")
    if not isinstance(to_exclude, int):
        raise ValueError(
            "Please input an integer between 1 and your sample size for to_exclude."
        )
    assert (
        len(t) - to_exclude
    ) >= 4, """The sample size for your model is smaller than 4. This will not produce a good
        model. Either reduce to_exclude or increase your sample size to continue."""
    assert y.notna().all(), f"""Your sample contains missing or infinite values for y at locations
        {list(map(tuple, np.where(np.isnan(y))))}. Exclude these values to continue."""
    assert t.notna().all(), f"""Your sample contains missing or infinite values for t at locations
        {list(map(tuple, np.where(np.isnan(t))))}. Exclude these values to continue."""

    # Convert date strings to numeric variables for the model
    if parse_dates:
        t_numeric = pd.to_datetime(t)
        t_numeric = (t_numeric - datetime(1970, 1, 1)).apply(lambda x: x.days)

    # Sort data by t increasing. t_ is for internal use.
    idx = np.argsort(t_numeric.values) if parse_dates else np.argsort(t.values)
    t_ = t_numeric[idx] if parse_dates else t[idx]
    t = t[idx]
    y = y[idx]

    results = pd.DataFrame()
    for degree in poly_features:
        transforms = make_pipeline(StandardScaler(), PolynomialFeatures(degree=degree))

        # Fit transforms to training data only, apply to all data.
        fitted_transforms = transforms.fit(t_[:-to_exclude].values.reshape(-1, 1))
        t_scaled = fitted_transforms.transform(t_.values.reshape(-1, 1))

        t_train, y_train = t_scaled[:-to_exclude, :], y[:-to_exclude]
        t_predict, y_predict, t_orig = (
            t_scaled if predict_all else t_scaled[-to_exclude:, :],
            y if predict_all else y[-to_exclude:],
            t if predict_all else t[-to_exclude:],
        )

        # Fit ordinary least squares model to the training data, then predict for the
        # prediction data.
        model = sm.OLS(y_train, t_train).fit()
        yhat = model.predict(t_predict)

        # Calculate prediction intervals of fitted model.
        _, yhat_l, yhat_u = wls_prediction_std(model, t_predict, alpha=alpha)

        # Store model results in master frame
        results = results.append(
            pd.DataFrame(
                {
                    "t": t_orig,
                    "yhat_u": yhat_u,
                    "yobs": y_predict,
                    "yhat": yhat,
                    "yhat_l": yhat_l,
                    "polynomial": degree,
                }
            ),
            ignore_index=True,
        )

    return results
