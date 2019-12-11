from codonPython import ref_decode
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SQL_connections import conn_DSS, conn_DSS2016UAT

test_df = pd.DataFrame([{'ORG_CODE': 'X24','ORG_CODE_answer': 'NHS ENGLAND','SNOMED_CODE': '74964007', 'SNOMED_CODE_answer' : 'Other (qualifier value)', 'ICD10_CODE': 'A00','ICD10_CODE_answer': 'Cholera'},
                           {'ORG_CODE': 'Q71','ORG_CODE_answer': 'NHS ENGLAND LONDON', 'SNOMED_CODE': '260413007', 'SNOMED_CODE_answer' : 'None', 'ICD10_CODE': 'A010','ICD10_CODE_answer': 'Typhoid fever'},
                           {'ORG_CODE': 'X26','ORG_CODE_answer': 'NHS DIGITAL', 'SNOMED_CODE': '276727009', 'SNOMED_CODE_answer' : 'Null', 'ICD10_CODE': 'A20','ICD10_CODE_answer': 'Plague'}])


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
