from codonPython.nhsNumberGenerator import nhsNumberGenerator 
import numpy as np
import pytest
import random


@pytest.mark.parametrize("to_generate, random_state, expected", [
    (20, 42, [
        7865793030,
        2195408316,
        1268550922,
        8962337908,
        3953104853,
        3629506283,
        3396707117,
        2498277064,
        8907799466,
        2100533533,
        8266005397,
        8952859324,
        6855828612,
        1933498560,
        7340365060,
        5530351107,
        1341263967,
        1319945236,
        2006045024,
        3347607384
        ]),
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