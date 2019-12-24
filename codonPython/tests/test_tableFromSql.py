from codonPython import tableFromSql
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import pytest
import sqlite3
import os

''' 
##################################### 
####  test plan for sqlfileToDf:
#####################################

    setup:
    - first need to make dummy sqlite3 database
    - then write dummy test.sql script
    
    test:
    - test the sqlfileToDf can read the file and return a df with the expected output
    
    cleanup:
    - remove the dummy test.sql script
'''
def make_dummy_sqlfile():
    sql_script = '''select CODE, NAME FROM (VALUES (1,'DOG'),(2,'CAT'), (3,'HORSE')) test(CODE,NAME)'''
    with open('test.sql', 'w') as file:
      file.write(sql_script)
    file.close()

    dummy_df = pd.DataFrame([dict(CODE=1, NAME='DOG'),
                             dict(CODE=2, NAME='CAT'),
                             dict(CODE=2, NAME='HORSE'), ])

    return dummy_df

def test_sqlfileToDf_output():
    # make sql database in memory
    conn = sqlite3.connect(':memory:')
    # make dummy file and corresponding df
    dummy_df = make_dummy_sqlfile()

    # assert that the output of the the function (reading the file) is the same as the expected df
    assert tableFromSql.sqlfileToDf('test.sql',conn) == dummy_df

    # cleanup file
    os.remove('test.sql')

if __name__ == '__main__':



#
#
#
#
# @pytest.mark.parametrize("age, expected", [
#     (0,  '0-4'),
#     (1,  '0-4'),
#     (12, '10-14'),
#     (23, '20-24'),
#     (34, '30-34'),
#     (35, '35-39'),
#     (46, '45-49'),
#     (57, '55-59'),
#     (68, '65-69'),
#     (79, '75-79'),
#     (90, '90 and over'),
# ])
# def test_age_band_5_years_BAU(age, expected):
#     assert expected == age_bands.age_band_5_years(age)
#
#
# def test_age_band_5_years_typeErrors():
#     with pytest.raises(TypeError):
#         age_bands.age_band_5_years("age")
