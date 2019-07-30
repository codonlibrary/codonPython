from codonPython.nhsNumberGenerator import nhsNumberGenerator 
import numpy as np
import pytest
import random


@pytest.mark.parametrize("to_generate, random_state, expected", [
    (3, 42, [7865793030, 1933498560, 7340365060]),
    (2, 1, [1677604360, 9170772010])
])
def test_nhsNumberGenerator_BAU(to_generate, random_state, expected):
    assert expected == nhsNumberGenerator(to_generate, random_state=random_state) 
