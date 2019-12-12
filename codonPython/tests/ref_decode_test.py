'''
Tests for functions in ref_decode_test.py

tests:
-------
ref_decode
  - test_ref_decode_col_num(): Test that function returns correct number of columns with different single column inputs
  - as this is largely dependent on org_col, sno_col and icd10_col, other tests are performed on those functions
org_code
  - test_org_col_col_num(): test correct number of columns
  - test_org_col_names(): test output org names are correct
'''

from codonPython import ref_decode
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SQL_connections import conn_DSS, conn_DSS2016UAT
import sqlite3
import pytest

test_df = pd.DataFrame([{'OrganisationCode': 'X24','Name': 'NHS ENGLAND',
                         'SNOMED_CODE': '74964007', 'SNOMED_CODE_answer' : 'Other (qualifier value)', 
                         'ICD10_CODE': 'A00','ICD10_CODE_answer': 'Cholera'},
                           {'OrganisationCode': 'Q71','Name': 'NHS ENGLAND LONDON', 
                            'SNOMED_CODE': '260413007', 'SNOMED_CODE_answer' : 'None', 
                            'ICD10_CODE': 'A010','ICD10_CODE_answer': 'Typhoid fever'},
                           {'OrganisationCode': 'X26','Name': 'NHS DIGITAL', 
                            'SNOMED_CODE': '276727009', 'SNOMED_CODE_answer' : 'Null', 
                            'ICD10_CODE': 'A20','ICD10_CODE_answer': 'Plague'}])

conn = sqlite3.connect(':memory:')
test_df_1 = pd.concat([test_df, 
                   test_df.rename(columns=dict(OrganisationCode='CCG'))[['CCG']],
                   test_df.rename(columns=dict(SNOMED_CODE='snomed'))[['snomed']],
                   test_df.rename(columns=dict(OrganisationCode='icd10'))[['icd10']],    
                  ],axis=1)
test_df_1.to_sql(test,conn)

@pytest.mark.parametrize("org_cols_test, sno_cols_test, icd10_cols_test, num_cols",
                         [('OrganisationCode', None, None, 1),
                          ('OrganisationCode', 'snomed', None, 2),
                          ('OrganisationCode', 'snomed', 'icd10', 3),
                          (None, 'snomed', 'icd10', 2),
                          (None, 'snomed', None, 1),
                          ('OrganisationCode', 'snomed', None, 2),
                          ('OrganisationCode', None, 'icd10', 2),
                          (None, None, 'icd10', 1),
                         ])
def test_ref_decode_col_num(org_cols_test, num_cols):
    df_out = ref_decode(test_df_1, 
                        org_cols=org_cols_test,
                        sno_cols=sno_cols_test,
                        icd10_cols=icd10_cols_test,
                        conn = conn)
    assert len(df_out.columns) == len(test_df_1) + num_cols
    
@pytest.mark.parametrize("org_cols_test, num_cols",
                         [('OrganisationCode', 1), # single item
                          (['OrganisationCode'], 1), # single item in list
                          (['OrganisationCode','CCG'], 2), # multiple items in list
                         ])
def test_org_col_col_num(org_cols_test, num_cols):
    df_out = org_col(test_df_1, 
                        org_cols=org_cols_test,
                        conn = conn)
    assert len(df_out.columns) == len(test_df_1) + num_cols
    
@pytest.mark.parametrize("org_cols_test, answer_cols",
                          (['OrganisationCode','CCG'], ['Name', 'Name']),
                         (['OrganisationCode'], ['Name']),
                         ('OrganisationCode', 'Name')
                         ])
def test_org_col_names(org_cols_test, answer_cols):
    df_out = org_col(test_df_1, 
                     org_cols=org_cols_test,
                     conn = conn)
    assert df_out[org_cols_test] == test_df_1[answer_cols]
