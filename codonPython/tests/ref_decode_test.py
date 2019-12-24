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
import pandas as pd
import sqlite3
import pytest
from pandas.util.testing import assert_frame_equal

test_df = pd.DataFrame([{'OrganisationCode': 'X24', 'Name': 'NHS ENGLAND',
                         'SNOMED_CODE': '74964007', 'SNOMED_CODE_answer': 'Other (qualifier value)',
                         'ICD10_CODE': 'A00', 'ICD10_CODE_answer': 'Cholera'},
                        {'OrganisationCode': 'Q71', 'Name': 'NHS ENGLAND LONDON',
                         'SNOMED_CODE': '260413007', 'SNOMED_CODE_answer': 'None',
                         'ICD10_CODE': 'A010', 'ICD10_CODE_answer': 'Typhoid fever'},
                        {'OrganisationCode': 'X26', 'Name': 'NHS DIGITAL',
                         'SNOMED_CODE': '276727009', 'SNOMED_CODE_answer': 'Null',
                         'ICD10_CODE': 'A20', 'ICD10_CODE_answer': 'Plague'}])

org_lkup = test_df.copy().set_index('OrganisationCode')['Name']
sno_lkp = test_df.copy().set_index('SNOMED_CODE')['SNOMED_CODE_answer'].rename('TERM')
icd10_lkp = test_df.copy().set_index('ICD10_CODE')['ICD10_CODE_answer'].rename('ICD10_DESCRIPTION')

test_df.rename(columns={'Name':'Answer'},inplace=True)

conn = sqlite3.connect(':memory:')
test_df_1 = pd.concat([test_df,
                       test_df.rename(columns=dict(OrganisationCode='CCG'))[['CCG']],
                       test_df.rename(columns=dict(SNOMED_CODE='snomed'))[['snomed']],
                       test_df.rename(columns=dict(OrganisationCode='icd10'))[['icd10']],
                       ], axis=1)
test_df_1.to_sql('test', conn)

# @pytest.mark.parametrize("org_cols_test, sno_cols_test, icd10_cols_test, num_cols",
#                          [('OrganisationCode', None, None, 1),
#                           ('OrganisationCode', 'snomed', None, 2),
#                           ('OrganisationCode', 'snomed', 'icd10', 3),
#                           (None, 'snomed', 'icd10', 2),
#                           (None, 'snomed', None, 1),
#                           ('OrganisationCode', 'snomed', None, 2),
#                           ('OrganisationCode', None, 'icd10', 2),
#                           (None, None, 'icd10', 1),
#                           ])
# def test_ref_decode_col_num(org_cols_test,sno_cols_test,icd10_cols_test,num_cols):
#     df_out = ref_decode.ref_decode(test_df_1,
#                         org_cols=org_cols_test,
#                         sno_cols=sno_cols_test,
#                         icd10_cols=icd10_cols_test,
#                         conn=conn)
#     assert len(df_out.columns) == len(test_df_1) + num_cols
#
#

# Org Cols tests
@pytest.mark.parametrize("org_cols_test, num_cols",
                         [('OrganisationCode', 1),  # single item
                          (['OrganisationCode'], 1),  # single item in list
                          (['OrganisationCode', 'CCG'], 2),  # multiple items in list
                          ])
def test_org_col_num(org_cols_test, num_cols):
    df_out = ref_decode.org_col(test_df_1,
                     org_cols_test,
                     org_lkp=org_lkup,
                     conn=conn)
    assert len(df_out.columns) == len(test_df_1.columns) + num_cols

@pytest.mark.parametrize("org_cols_test, output_col, answer_cols",
                         [(['OrganisationCode', 'CCG'], ['OrganisationCode_name','CCG_name'],['Answer', 'Answer']),
                         (['OrganisationCode'], ['OrganisationCode_name'], ['Answer']),
                         ('OrganisationCode', 'OrganisationCode_name', 'Answer')
                          ])
def test_org_col_names(org_cols_test, output_col, answer_cols):
    df_out = ref_decode.org_col(test_df_1,
                     org_cols_test,
                     org_lkp = org_lkup)

    if type(answer_cols) != list:
        answer_cols = [answer_cols]
        output_col = [output_col]
    answer = test_df_1[answer_cols].copy()
    answer.columns = df_out[output_col].columns
    assert_frame_equal(df_out[output_col], answer,check_names=False)

# Sno Col tests
@pytest.mark.parametrize("cols_test, num_cols",
                         [('SNOMED_CODE', 1),  # single item
                          (['SNOMED_CODE'], 1),  # single item in list
                          (['SNOMED_CODE', 'snomed'], 2),  # multiple items in list
                          ])
def test_sno_col_num(cols_test, num_cols):
    df_out = ref_decode.sno_col(test_df_1,
                     cols_test,
                     df_sno_lkp=sno_lkp,
                     conn=conn)
    assert len(df_out.columns) == len(test_df_1.columns) + num_cols

# @pytest.mark.parametrize("org_cols_test, output_col, answer_cols",
#                          [(['OrganisationCode', 'CCG'], ['OrganisationCode_name','CCG_name'],['Answer', 'Answer']),
#                          (['OrganisationCode'], ['OrganisationCode_name'], ['Answer']),
#                          ('OrganisationCode', 'OrganisationCode_name', 'Answer')
#                           ])
# def test_sno_col_names(org_cols_test, output_col, answer_cols):
#     df_out = ref_decode.sno_col(test_df_1,
#                      org_cols_test,
#                      org_lkp = org_lkup)
#
#     if type(answer_cols) != list:
#         answer_cols = [answer_cols]
#         output_col = [output_col]
#     answer = test_df_1[answer_cols].copy()
#     answer.columns = df_out[output_col].columns
#     assert_frame_equal(df_out[output_col], answer,check_names=False)
