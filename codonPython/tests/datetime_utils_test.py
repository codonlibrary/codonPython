from codonPython.datetime_utils import add_time
#import pytest

#------------------------------add_time----------------------------------------

@pytest.mark.parametrize("date, years, months, days, expected", [
    ('2019-01-01', 1, 2,3, '2020-03-04')])

def test_add_time_all(date, years, months, days, expected):
    assert add_time(date, years=years, months=months, days=days) == expected


@pytest.mark.parametrize("date, years, expected", [
    ('2019-01-01', -2, '2017-01-01')])

def test_add_time_years(date, years, expected):
    assert add_time(date, years=years) == expected


@pytest.mark.parametrize("date, months, expected", [
    ('2019-01-01', 5, '2019-06-01')])

def test_add_time_months(date, months, expected):
    assert add_time(date, months=months) == expected


@pytest.mark.parametrize("date, days, expected", [
    ('2019-01-01', 49, '2019-02-19')])

def test_add_time_days(date, days, expected):
    assert add_time(date, days=days) == expected
