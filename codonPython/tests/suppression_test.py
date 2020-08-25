from codonPython.suppression import central_suppresion_method
import pytest


@pytest.mark.parametrize(
    "to_suppress, expected",
    [(0, "0"), (2, "5"), (5, "5"), (8, "10"), (16, "15"), (57, "55"), (10023, "10025")],
)
def test_central_suppresion_method_BAU(to_suppress, expected):
    assert expected == central_suppresion_method(to_suppress)


@pytest.mark.parametrize("to_suppress", [-1, 4.2, 5000000001])
def test_suppress_value_valueErrors(to_suppress):
    with pytest.raises(ValueError):
        central_suppresion_method(to_suppress)
