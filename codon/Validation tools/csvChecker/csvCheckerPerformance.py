"""Validate CSV file with 100k rows to test performance
"""

from vladiate import Vlad
from vladiate.validators import (
    NotEmptyValidator,
    Ignore,
    IntValidator,
    RegexValidator,
    UniqueValidator,
    SetValidator,
)
from vladiate.inputs import LocalFile
import time

# To validate a CSV file, a validator subclass of class "Vlad" is made for it's schema.
# This specifies all the columns and rules for their contents.
class bigValidator(Vlad):
    validators = {
        'Region' : [NotEmptyValidator()],
        'Country' : [Ignore()],
        'Item Type' : [Ignore()],
        'Sales Channel' : [SetValidator(['Offline', 'Online'])],
        'Order Priority' : [SetValidator(['C', 'L', 'M', 'H'])],
        'Order Date' : [
            RegexValidator(
                pattern=r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
            )
        ],  # This pretty huge RegEx expression validates that a sensible dd/mm/yyyy date has been input
        'Order ID' : [UniqueValidator()],
        'Ship Date' : [
            RegexValidator(
                pattern=r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
            )
        ],  # This pretty huge RegEx expression validates that a sensible dd/mm/yyyy date has been input
        'Units Sold' : [IntValidator()],
        'Unit Price' : [Ignore()],
        'Unit Cost' : [Ignore()],
        'Total Revenue' : [Ignore()],
        'Total Cost' : [Ignore()],
        'Total Profit' :  [Ignore()],
    }

# Now, check the time required to check a 100k x 10 df

s = time.time()
bigValidator(source=LocalFile('100kTest.csv')).validate()
e = time.time()
print('Runtime :', (e-s), 'seconds for 100.000 rows')