''' Author(s): Sam Hollings
Desc: This module contains various functions to decode reference data into a description, which will be widely used across projects.
Contents:
    org_col()
    sno_col()
    icd10_col()
'''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SQL_connections import conn_DSS, conn_DSS2016UAT


def org_col(df, column):
    '''Desc: Converts column of org_codes into organisation names using DSS Org tables.
        df - pd.DataFrame with a column of organisation codes
        column - column name with Org codes
    Returns: submitted df with additional column+"_name" with corresponding organisation code names'''
    import common_python.DSS_org_import as org
    df_org = org.dss_org_api()
    df_org_lkp = df_org[['OrganisationId', 'Name']].rename(columns={'OrganisationId': 'ORG_CODE', 'Name': 'NAME'})
    df_org_idx = df_org_lkp.set_index('ORG_CODE')['NAME']  # this allows us to pull names easily

    df_org_col = df.join(df_org_idx, on=column).rename(columns={'NAME': column + '_name'})
    return df_org_col


def org_col_list(df, column_list):
    '''Desc: Converts column of org_codes into organisation names using DSS Org tables.
        df - pd.DataFrame with a column of organisation codes
        column - column name with Org codes
    Returns: submitted df with additional column+"_name" with corresponding organisation code names'''
    import common_python.DSS_org_import as org
    df_org = org.dss_org_api()
    df_org_lkp = df_org[['OrganisationId', 'Name']].rename(columns={'OrganisationId': 'ORG_CODE', 'Name': 'NAME'})
    df_org_idx = df_org_lkp.set_index('ORG_CODE')['NAME']  # this allows us to pull names easily

    for column in column_list:
        df = df.join(df_org_idx, on=column).rename(columns={'NAME': column + '_name'})
    return df


def sno_col(df, column):
    '''Desc: Converts column of SNOMED codes into SNOMED descriptions (TERMs) using DSS SNOMED tables.
        df - pd.DataFrame with a column of SNOMED codes
        column - column name with SNOMED codes
    Returns: submitted df with additional column+"_desc" with corresponding SNOMED TERMs'''
    import common_python.DSS_clinical_codes as cc
    df_SNO = cc.SNO_lkp()
    df_SNO_indxd = df_SNO.set_index('CONCEPT_ID')
    df_sno_col = df.join(df_SNO_indxd, on=column).rename(columns={'TERM': column + '_desc'})
    return df_sno_col


def sno_col_list(df, column_list):
    '''Desc: Converts column of SNOMED codes into SNOMED descriptions (TERMs) using DSS SNOMED tables.
        df - pd.DataFrame with a column of SNOMED codes
        column - column name with SNOMED codes
    Returns: submitted df with additional column+"_desc" with corresponding SNOMED TERMs'''
    import common_python.DSS_clinical_codes as cc
    df_SNO = cc.SNO_lkp()
    df_SNO_indxd = df_SNO.set_index('CONCEPT_ID')
    for column in column_list:
        print('sno_col: ', column)
        df = df.join(df_SNO_indxd, on=column).rename(columns={'TERM': column + '_desc'})
    return df


def icd10_col(df, column, fourchar=False):
    '''Desc: Converts column of ICD10 codes into ICD10 descriptions using DSS ICD10 tables.
        df - pd.DataFrame with a column of ICD10 codes
        column - column name with ICD10 codes
    Returns: submitted df with additional column+"_desc" with corresponding ICD10 descriptions'''
    import common_python.DSS_clinical_codes as cc

    if fourchar is True:
        code = 'CODE'
    else:
        code = 'ALT_CODE'
    df_icd10 = cc.ICD10_lkp()[[code, 'ICD10_DESCRIPTION']]
    df_icd10_indxd = df_icd10.set_index(code)
    df_icd10_col = (df.join(df_icd10_indxd, on=column, how='left')
                    .rename(columns={'ICD10_DESCRIPTION': column + '_desc'}))
    return df_icd10_col
