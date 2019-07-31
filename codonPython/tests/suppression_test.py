# from codonpython.suppression import suppression
import pandas as pd
import pytest

@pytest.mark.parametrize("to_suppress, expected", [
    (
        pd.DataFrame({"count":[0,2,4,6,8,10,101,1001]}), 
        pd.DataFrame({"count":[0,"*","*","*",10,10,100,1000]})
    )
])
def test_supression_BAU(to_generate, random_state, expected):
    assert expected == suppression(to_generate, random_state=random_state) 

@pytest.mark.parametrize("to_suppress", [
    pd.DataFrame({"count":[0,-2,4,6,8,10,101,1001]}),
    pd.DataFrame({"count":[0,2,4,6,8,10,101,100000000]}),
    pd.DataFrame({"count":[0,2.2,4,6,8,10,101,1001]})
])
def test_supression_valueErrors(to_generate):  
    with pytest.raises(ValueError): 
        suppression(to_generate)