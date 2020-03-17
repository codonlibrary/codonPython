from codonPython.nhsNumber import nhsNumberGenerator, nhsNumberValidator
import pytest
import random


@pytest.mark.parametrize(
    "to_generate, random_state, expected",
    [(3, 42, [7065337065, 6104866670, 4417443181]), (2, 1, [6446801785, 4227327237])],
)
def test_nhsNumberGenerator_BAU(to_generate, random_state, expected):
    assert expected == nhsNumberGenerator(to_generate, random_state=random_state)


@pytest.mark.parametrize(
    "to_generate, random_state", [(100, 111), (100, None), (100, 999)],
)
def test_nhsNumberGenerator_makesValid(to_generate, random_state):
    assert all(
        (
            nhsNumberValidator(val)
            for val in nhsNumberGenerator(to_generate, random_state=random_state)
        )
    )


@pytest.mark.parametrize("to_generate", [4.2, -1])
def test_nhsNumberGenerator_valueErrors(to_generate):
    with pytest.raises(ValueError):
        nhsNumberGenerator(to_generate)


@pytest.mark.parametrize(
    "to_validate, expected", [(6771116069, True), (9598980007, False)]
)
def test_nhsNumberValidator_BAU(to_validate, expected):
    assert expected == nhsNumberValidator(to_validate)


@pytest.mark.parametrize("to_validate", [4.2, 1000001, -1])
def test_nhsNumberValidator_valueErrors(to_validate):
    with pytest.raises(ValueError):
        nhsNumberValidator(to_validate)
