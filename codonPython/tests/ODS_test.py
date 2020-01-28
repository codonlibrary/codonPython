import pytest
import numpy as np
from codonPython.ODS_lookup import query_ods_api, get_addresses


def test_successful_query():
    NHSD_code = "X26"
    result = query_ods_api(NHSD_code)
    assert result["Organisation"]["Name"] == "NHS DIGITAL"


def test_unsuccessful_query():
    invalid_code = "ASDF"
    with pytest.raises(ValueError):
        query_ods_api(invalid_code)


def test_wrong_type():
    invalid_code = 0
    with pytest.raises(ValueError):
        query_ods_api(invalid_code)


def test_unsuccessful_address_query():
    invalid_code = ["ASDF", np.nan, None]
    result = get_addresses(invalid_code)
    assert result.empty
