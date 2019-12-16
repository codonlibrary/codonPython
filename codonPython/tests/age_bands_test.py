from codonPython import age_bands
import numpy as np
import math
import pytest


@pytest.mark.parametrize(
    "age, expected",
    [
        (0, "0-4"),
        (1, "0-4"),
        (12, "10-14"),
        (23, "20-24"),
        (34, "30-34"),
        (35, "35-39"),
        (46, "45-49"),
        (57, "55-59"),
        (68, "65-69"),
        (79, "75-79"),
        (90, "90 and over"),
    ],
)
def test_age_band_5_years_BAU(age, expected):
    assert expected == age_bands.age_band_5_years(age)


def test_age_band_5_years_typeErrors():
    with pytest.raises(TypeError):
        age_bands.age_band_5_years("age")


@pytest.mark.parametrize("age", [np.nan, math.inf, -3, 343, -0.1])
def test_age_band_5_years_valueErrors(age):
    with pytest.raises(ValueError):
        age_bands.age_band_5_years(age)


@pytest.mark.parametrize("age, expected", [(None, "Age not known")])
def test_age_band_5_years_edgeCases(age, expected):
    assert expected == age_bands.age_band_5_years(age)


@pytest.mark.parametrize(
    "age, expected",
    [
        (0.1, "0-4"),
        (1.2, "0-4"),
        (12.3, "10-14"),
        (23.4, "20-24"),
        (34.5, "30-34"),
        (35.6, "35-39"),
        (46.7, "45-49"),
        (57.8, "55-59"),
        (68.9, "65-69"),
        (79.0, "75-79"),
        (90.1, "90 and over"),
    ],
)
def test_age_band_5_years_BAU_floats(age, expected):
    assert expected == age_bands.age_band_5_years(age)


@pytest.mark.parametrize(
    "age, expected",
    [
        (0, "0-9"),
        (1, "0-9"),
        (12, "10-19"),
        (23, "20-29"),
        (34, "30-39"),
        (35, "30-39"),
        (46, "40-49"),
        (57, "50-59"),
        (68, "60-69"),
        (79, "70-79"),
        (90, "90 and over"),
    ],
)
def test_age_band_10_years_BAU(age, expected):
    assert expected == age_bands.age_band_10_years(age)


def test_age_band_10_years_typeErrors():
    with pytest.raises(TypeError):
        age_bands.age_band_10_years("age")


@pytest.mark.parametrize("age", [np.nan, math.inf, -3, 343, -0.1])
def test_age_band_10_years_valueErrors(age):
    with pytest.raises(ValueError):
        age_bands.age_band_10_years(age)


@pytest.mark.parametrize("age, expected", [(None, "Age not known")])
def test_age_band_10_years_edgeCases(age, expected):
    assert expected == age_bands.age_band_10_years(age)


@pytest.mark.parametrize(
    "age, expected",
    [
        (0.1, "0-9"),
        (1.2, "0-9"),
        (12.3, "10-19"),
        (23.4, "20-29"),
        (34.5, "30-39"),
        (35.6, "30-39"),
        (46.7, "40-49"),
        (57.8, "50-59"),
        (68.9, "60-69"),
        (79.0, "70-79"),
        (90.1, "90 and over"),
    ],
)
def test_age_band_10_years_BAU_floats(age, expected):
    assert expected == age_bands.age_band_10_years(age)
