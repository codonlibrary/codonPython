import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


def check_tolerance(X, y, to_exclude: int = 1, poly_features: int = 2, alpha: float = 0.05) -> pd.DataFrame:
    """
    Check that some future values are within a weighted least squares confidence interval.

    Parameters
    ----------
    X : np.array
        N independent variables of shape (N, 1).
    y : np.array
        The corresponding dependent variable values to X, of shape (N, 1).
    to_exclude : int, default = 1
        How many of the last y values will have their tolerances checked.
    poly_features : int, default = 2
        Degree of polynomial features to fit to the data.
    alpha : float, default = 0.05
        Alpha parameter for the weighted least squares confidence interval.


    Returns
    -------
    pd.DataFrame
        DataFrame of shape (to_exclude, 4) containing:
            "yhat_u" : Upper condfidence interval for y
            "yobs"   : Observed value for y
            "yhat"   : Predicted value for y
            "yhat_l" : Lower confidence interval for y


    Examples
    --------
    >>> check_tolerance(
    ...     X = np.array([1001,1002,1003,1004,1005]),
    ...     y = np.array([2,3,4,4.5,5])
    ... ).round(3).to_dict()
    {'yhat_u': {0: 9.077}, 'yobs': {0: 5.0}, 'yhat': {0: 4.875}, 'yhat_l': {0: 0.673}}
    """

    if not isinstance(poly_features, int) or 0 >= poly_features >= 4:
        raise ValueError("Please input an integer from 0 to 4 for poly_features.")
    if not isinstance(alpha, float) or 0 >= alpha >= 1:
        raise ValueError("Please input a float between 0 and 1 for alpha.")

    N = len(X)

    if not isinstance(to_exclude, int) or N <= to_exclude < 1:
        raise ValueError("Please input an integer between 1 and your sample size to exclude.")
    if N < 4:
        raise ValueError("Your sample size is smaller than 4. This will not produce a good model.")

    # Sort data by X increasing
    idx = np.argsort(X)
    X = X[idx]
    y = y[idx]

    transforms = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=poly_features),
    )

    # Fit transforms to train data, apply them to all data
    fitted_transforms = transforms.fit(X[:to_exclude].reshape(-1, 1))
    X = fitted_transforms.transform(X.reshape(-1, 1))

    X_train, y_train = X[:-to_exclude, :], y[:-to_exclude]
    X_predict, y_predict = X[(N-to_exclude):, :], y[(N-to_exclude):]

    # Fit ordinary least squares model to the training data, then predict for the 
    # prediction data.
    model = sm.OLS(y_train, X_train).fit()
    yhat = model.predict(X_predict)

    # Calculate confidence interval of fitted model.
    _, yhat_l, yhat_u = wls_prediction_std(model, X_predict, alpha=alpha)

    return pd.DataFrame({
        "yhat_u" : yhat_u,
        "yobs" : y_predict,
        "yhat" : yhat,
        "yhat_l" : yhat_l,
    })
