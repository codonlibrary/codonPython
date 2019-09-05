import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


def check_tolerance(t, y, to_exclude: int = 1, poly_features: list = [1, 2], alpha: float = 0.05, forecast: bool = False) -> pd.DataFrame:
    """
    Check that some future values are within a weighted least squares confidence interval.

    Parameters
    ----------
    t : np.array
        N explanatory time bins of shape (N, 1).
    y : np.array
        The corresponding response variable values to X, of shape (N, 1).
    to_exclude : int, default = 1
        How many of the last y values will have their tolerances checked.
    poly_features : list, default = [1, 2]
        List of degrees of polynomial features to fit to the data. One model will be
        produced for each number in the list, eg. the default will fit a linear and
        a second degree polynomial to the data and return both sets of results.
    alpha : float, default = 0.05
        Alpha parameter for the weighted least squares confidence interval.
    forecast : bool, default = False
        When set to true, will return model projections for 20% of the data range beyond
        the current distribution.


    Returns
    -------
    pd.DataFrame
        DataFrame of shape (to_exclude, 4) containing:
            "yhat_u"    : Upper condfidence interval for y
            "yobs"      : Observed value for y
            "yhat"      : Predicted value for y
            "yhat_l"    : Lower confidence interval for y
            "polynomial": Max polynomial of model fit to the data


    Examples
    --------
    >>> check_tolerance(
    ...     t = np.array([1001,1002,1003,1004,1005,1006]),
    ...     y = np.array([2,3,4,4.5,5,5.1]),
    ...     to_exclude = 2,
    ... )
          yhat_u  yobs   yhat    yhat_l  polynomial
    0   6.817413   5.0  5.500  4.182587           1
    1   7.952702   5.1  6.350  4.747298           1
    2   9.077182   5.0  4.875  0.672818           2
    3  13.252339   5.1  4.975 -3.302339           2
    """

    if not isinstance(poly_features, list):
        raise ValueError("Please input a list of integers from 0 to 4 for poly_features.")
    assert all(0 <= degree <= 4 for degree in poly_features), (
      "Please ensure all numbers in poly_features are from 0 to 4."  
    )
    if not isinstance(alpha, float) or 0 >= alpha >= 1:
        raise ValueError("Please input a float between 0 and 1 for alpha.")
    if not isinstance(to_exclude, int) or len(t) <= to_exclude < 1:
        raise ValueError("Please input an integer between 1 and your sample size for to_exclude.")
    assert ((len(t) - to_exclude) >= 4), (
        """The sample size for your model is smaller than 4. This will not produce a good 
        model. Either reduce to_exclude or increase your sample size to continue."""
    )
    assert np.isfinite(y).all(), (
        "Your sample contains missing or infinite values for y. Exclude these values to continue."
    )


    # Sort data by X increasing
    idx = np.argsort(t)
    t = t[idx]
    y = y[idx]
    forecasts = 5

    if forecast:
        # 5 forecast values based on 20% of data range
        t_range = t[-1] - t[0]
        t_forecast = np.linspace(
            (t[-1] + t_range*0.001),
            (t[-1] + t_range*0.2),
            forecasts,
        )
    
    results = pd.DataFrame()
    for degree in poly_features:
        transforms = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(degree=degree),
        )

        # Fit transforms to training data only, apply to all data.
        fitted_transforms = transforms.fit(t[:-to_exclude].reshape(-1, 1))
        _t = fitted_transforms.transform(t.reshape(-1, 1))

        t_train, y_train = _t[:-to_exclude, :], y[:-to_exclude]
        t_predict, y_predict = _t[-to_exclude:, :], y[-to_exclude:]
    
        if forecast:
            # Add forecasts to prediction array
            t_predict = np.append(
                t_predict,
                fitted_transforms.transform(t_forecast.reshape(-1, 1)),
                axis=0
            )
            # This will prevent the final dataframe complaining about array lengths.
            y_predict = np.append(y_predict, np.full(forecasts, np.nan))
        
        # Fit ordinary least squares model to the training data, then predict for the
        # prediction data.
        model = sm.OLS(y_train, t_train).fit()
        yhat = model.predict(t_predict)

        # Calculate confidence interval of fitted model.
        _, yhat_l, yhat_u = wls_prediction_std(model, t_predict, alpha=alpha)

        # Store model results in master frame
        results = results.append(
            pd.DataFrame({
              "yhat_u" : yhat_u,
              "yobs" : y_predict,
              "yhat" : yhat,
              "yhat_l" : yhat_l,  
              "polynomial" : degree
            }),
            ignore_index=True,
        )

    return results
    