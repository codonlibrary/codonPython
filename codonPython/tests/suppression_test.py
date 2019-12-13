from codonPython.suppression import suppress_value
import pytest


@pytest.mark.parametrize(
    "to_suppress, expected",
    [(0, "0"), (2, "*"), (5, "*"), (8, "10"), (16, "15"), (57, "55"), (10023, "10025")],
)
def test_suppress_value_BAU(to_suppress, expected):
    assert expected == suppress_value(to_suppress)


@pytest.mark.parametrize("to_suppress", [-1, 4.2, 100000001])
def test_suppress_value_valueErrors(to_suppress):
    with pytest.raises(ValueError):
        suppress_value(to_suppress)
