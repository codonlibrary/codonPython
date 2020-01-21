import numpy as np
from numpy.random import default_rng


def nhsNumberValidator(number: int) -> bool:
    """
    Validate NHS Number according to modulus 11 checks as recorded in the data dictionary.
    https://www.datadictionary.nhs.uk/data_dictionary/attributes/n/nhs/nhs_number_de.asp?shownav=1

    Parameters
    ----------
    number : int
        10 digit integer to validate.

    Returns
    ----------
    bool
        If the number passes modulus 11 checks a.k.a. is valid.

    Examples
    ---------
    >>> nhsNumberValidator(8429141456)
    True
    >>> nhsNumberValidator(8429141457)
    False
    """

    if not isinstance(number, int):
        raise ValueError("Please input a positive 10 digit integer to validate.")
    if number < 0:
        raise ValueError("Please input a postitive 10 digit integer to validate.")
    digits = [int(digit) for digit in str(number)]
    # NHS Numbers are 10 digits long.
    if not len(digits) == 10:
        raise ValueError("Please input a postitive 10 digit integer to validate.")
    # Apply weighting to first 9 digits
    weighted_digits = np.dot(np.array(digits[:9]), np.arange(10, 1, -1))
    # Validity is based on the check digit, which has to be equal to `remainder`
    remainder = weighted_digits % 11
    check_digit = 11 - remainder
    if check_digit == 11:
        check_digit = 0
    if check_digit == digits[-1]:
        return True
    else:
        return False


def nhsNumberGenerator(to_generate: int, random_state: int = None) -> list:
    """
    Generates random NHS numbers compliant with modulus 11 checks as recorded
    in the data dictonary.
    https://www.datadictionary.nhs.uk/data_dictionary/attributes/n/nhs/nhs_number_de.asp?shownav=1

    Parameters
    ----------
    to_generate : int
        number of NHS numbers to generate
    random_state : int, default : None
        Optional seed for random number generation, for testing and reproducibility.

    Returns
    ----------
    generated : list
        List of randomly generated valid NHS numbers

    Examples
    ---------
    >>> nhsNumberGenerator(2, random_state=42)
    [8429141456, 2625792787]
    """

    if not isinstance(to_generate, int):
        raise ValueError("Please input a positive integer to generate numbers.")
    if to_generate < 0:
        raise ValueError("Please input a postitive integer to generate numbers.")
    rng = default_rng(random_state)

    # The NHS numbers are generated in three stages.
    #   First, generate 8 digits, using numpy.randint (the middle 8 digits)
    #   Second, generate the check digit portions for each block of 8 digits
    #   Third, generate 1 digit (the 1st digit) between 1 and 8
    #       increase this value by 1 if it is at or above the value which would cause a check digit of 10
    #       be aware that this will not produce a fully uniform distribution over NHS numbers
    #       the distribution will not produce any NHS number with a leading digit (or check digit) of 1 where the
    #       contribution of the middle 8 digits to the check digit is 0
    #   Fourth, generate the check digit from the above values
    #   Fifth, combine the digits into a number
    base_number = rng.integers(0, 9, size=(to_generate, 8), dtype=np.int32)
    check_digit_portion = np.vstack(np.dot(base_number, np.arange(9, 1, -1)) % 11)
    leading_candidate = rng.integers(1, 8, size=(to_generate, 1), dtype=np.int32)

    # The resulting check digit is x_10 - k, where k is the contribution of the other digits
    # Then the check digit would be 10 (invalid) if the leading digit were k+10 mod 11, or equally, k-1
    leading_digit = leading_candidate + (leading_candidate >= check_digit_portion - 1)
    check_digit = (leading_digit - check_digit_portion) % 11
    result_digits = np.hstack([leading_digit, base_number, check_digit])

    result = np.dot(result_digits, 10**np.arange(9, -1, -1, dtype=np.int64))
    
    return list(result)
