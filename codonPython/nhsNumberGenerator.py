import random
import numpy as np


def nhsNumberGenerator(to_generate: int, random_state: int = None)->list:
    """
    Generates up to 1M random NHS number(s) compliant with modulus 11 checks recorded 
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
        List of randomly generated NHS numbers

    Examples
    ---------
    >>> nhsNumberGenerator(2, random_state=42)
    [7865793030, 2195408316]
    """

    if random_state:
        random.seed(random_state)
    if not isinstance(to_generate, int):
        raise ValueError("Please input a positive integer to generate numbers.")
    if to_generate > 1000000:
        raise ValueError("More than one million values requested")
    if to_generate < 0:
        raise ValueError("Please input a postitive integer to generate numbers.")

    generated = []
    while len(generated) < to_generate:
        # Random 9 digit number starting with non-zero digit
        number = random.randint(100000000, 999999999)
        digits = [int(digit) for digit in str(number)]
        # Apply weighting to digits
        weighted_digits = np.dot(np.array(digits), np.arange(10,1,-1))
        # Validity is based on the check digit, which can't be 10   
        remainder = weighted_digits % 11
        check_digit = 11 - remainder
        if check_digit == 10:
            continue
        if check_digit == 11: 
            check_digit = 0
        # Add check digit to valid number
        number = int(str(number) + str(check_digit))
        generated.append(number)
    return generated
