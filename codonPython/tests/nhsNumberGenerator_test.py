from codonPython.nhsNumberGenerator import nhsNumberGenerator 
import numpy as np
import pytest
import random


@pytest.mark.parametrize("to_generate, random_state, expected", [
    (3, 42, [7865793030, 2195408316, 1268550922]),
    (2, 1, [2442725096, 7111780027])
])
def test_nhsNumberGenerator_BAU(to_generate, random_state, expected):
    assert expected == nhsNumberGenerator(to_generate, random_state=random_state) 

@pytest.mark.parametrize("to_generate", [
    4.2,
    1000001,
    -1
])
def test_nhsNumberGenerator_valueErrors(to_generate):  
    with pytest.raises(ValueError): 
        nhsNumberGenerator(to_generate)