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

ref_decode(df, org_cols=[], sno_cols=[], icd10_cols=[])

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
def test_ref_decode_col_num():
    df_out = ref_decode(test_df_1, 
                        org_cols=org_cols_test,
                        sno_cols=sno_cols_test,
                        icd10_cols=icd10_cols_test)
    assert len(df_out.columns) == len(test_df_1) + num_cols
    
                        
    
    

class Test_sno_col(unittest.TestCase):
    # Test the "sno_col()" function
    def setUp(self):

        sno_df = cf.sno_col(test_df,'SNOMED_CODE')
        self.SNOMED_desc = sno_df['SNOMED_CODE_desc']

    def test_desc_col(self):
        self.assertIn(self.SNOMED_desc.iloc[0],test_df['SNOMED_CODE_answer'].iloc[0])

class Test_org_col(unittest.TestCase):
    # Test the "sno_col()" function
    def setUp(self):

        df = cf.org_col(test_df,'ORG_CODE')
        self.ORG_desc = df['ORG_CODE_name']

    def test_desc_col(self):
        self.assertIn(self.ORG_desc.iloc[0],test_df['ORG_CODE_answer'].iloc[0])
