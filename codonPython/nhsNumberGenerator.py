import random


def nhsNumberGenerator(to_generate: int, random_state: int = None)->list:
    """
    Generates random NHS number(s) compliant with modulus 11 checks recorded 
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
    [7865793030, 1933498560]
    """

    if random_state:
        random.seed(random_state)
        
    generated = []
    while len(generated) < to_generate:
        # Random 9 digit number starting with non-zero digit
        number = random.randint(100000000, 999999999)
        digits = [int(digit) for digit in str(number)]
        # Apply weighting to digits
        weighted_digits = [(10 - index) * digit for (index, digit) in enumerate(digits)]
        # Sum of all weighted digits must be a multiple of 11 to be valid.
        if sum(weighted_digits) % 11 == 0:
            # Add check digit to valid number
            number = int(str(number) + "0")
            generated.append(number)
    return generated
