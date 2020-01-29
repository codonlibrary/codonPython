import requests
from typing import Dict, Iterable, Callable, List, Optional
import pandas as pd
import numpy as np


def query_api(code: str) -> Dict:
    """Query the ODS (organisation data service) API for a single org code
    and return the full JSON result. Full API docs can be found here:
    https://digital.nhs.uk/services/organisation-data-service/guidance-for-developers/organisation-endpoint

    Parameters
    ----------
    code : str
        3 character organization code.

    Returns
    ----------
    dict
        The data returned from the API.

    Examples
    ---------
    >>> result = query_api("X26")
    >>> result["Organisation"]["Name"]
    'NHS DIGITAL'
    >>> result["Organisation"]["GeoLoc"]["Location"]["AddrLn1"]
    '1 TREVELYAN SQUARE'
    """
    if not isinstance(code, str):
        raise ValueError(f"ODS code must be a string, received {type(code)}")

    response = requests.get(
        f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/{code}"
    ).json()
    if "errorCode" in response:
        error_code = response["errorCode"]
        error_text = response["errorText"]
        raise ValueError(
            f"API query failed with code {error_code} and text '{error_text}'."
        )
    return response


def get_addresses(codes: Iterable[str]) -> pd.DataFrame:
    """Query the ODS (organisation data service) API for a series of
    org codes and return a data frame containing names and addresses.
    Invalid codes will cause a message to be printed but will
    otherwise be ignored, as an incomplete merge table is more
    useful than no table at all.

    Parameters
    ----------
    codes : list, ndarray or pd.Series
        3 character organization codes to retrieve information for.

    Returns
    ----------
    DataFrame
        Address information for the given org codes.

    Examples
    ---------
    >>> result = get_addresses(pd.Series(["X26"]))
    >>> result.reindex(columns=sorted(result.columns))
              Org_AddrLn1 Org_Code Org_Country     Org_Name Org_PostCode Org_Town
    0  1 TREVELYAN SQUARE      X26     ENGLAND  NHS Digital      LS1 6AE    LEEDS
    """

    # Internal helper function to take the full result of a query
    # and extract the relevant fields
    def extract_data(api_result: Dict, code: str) -> Dict[str, str]:
        org_info = api_result["Organisation"]
        org_name = org_info["Name"]
        org_address = org_info["GeoLoc"]["Location"]
        result = {
            "Org_Code": code,
            "Org_Name": org_name.title().replace("Nhs", "NHS"),
            **{f"Org_{k}": v for k, v in org_address.items() if k != "UPRN"},
        }
        return result

    # Remove duplicate values
    to_query = set(codes)
    if np.nan in to_query:
        # 'NaN' is actually a valid code but we don't want it for null values
        to_query.remove(np.nan)

    result = []
    for code in to_query:
        try:
            api_result = query_api(code)
            result.append(extract_data(api_result, code))
        except ValueError as e:
            print(f"No result for ODS code {code}. {e}")
            continue
    return pd.DataFrame(result)
