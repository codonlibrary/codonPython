''' Author(s): Sam Hollings
Desc: This module contains various functions to decode reference data into a description, which will be widely used across projects.
Contents:
    ref_decode()
    org_col()
    sno_col()
    icd10_col()
    dss_org_api()
    ICD10_lkp()
    SNO_lkp()
'''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SQL_connections import conn_DSS, conn_DSS2016UAT

''''Main Function'''
def ref_decode(df, org_cols=[], sno_cols=[], icd10_cols=[], conn=conn_DSS2016UAT()):
    '''Converts the org codes, SNOMED codes and ICD10 codes in the supplied columns of the supplied 
    dataframe into the corresponding names/descriptions.
    Inputs:
    -------
    df : pandas.DataFrame
        Dataframe containing columns which you want to decode
    org_cols : list
        list of names of columns in "df" which contain ORG_CODES you want to decode into Org names
    sno_cols : list
        list of names of columns in "df" which contain SNOMED codes you want to decode into SNOMED concepts
    icd10_cols : list
        list of names of columns in "df" which contain ICD10 codes you want to decode into ICD10 descriptions
    
    returns:
    --------
    df_decoded : pandas.DataFrame
        Dataframe as "df", however with new columns containing the decoded names/descriptions.
    '''
    df_decoded = df.copy()
    if org_cols != []:
        df_decoded = org_col(df_decoded,org_cols,conn=conn)
    if sno_cols != []:
        df_decoded = sno_col(df_decoded,sno_cols,conn=conn)
    if icd10_cols != []:
        df_decoded = icd10_col(df_decoded,icd10_cols,conn=conn)
    return df_decoded

'''Sub functions'''
def org_col(df, column_list, org_lkp=None, conn=conn_DSS2016UAT()):
    '''Desc: Converts column of org_codes into organisation names using DSS Org tables.
    inputs:
    -------
     df : pd.DataFrame
        dataframe with a column of organisation codes
    column_list : list
        list of column names with Org codes
    Returns:
    --------
    df : pd.DataFrame
        submitted df with additional columns called column+"_name" with corresponding organisation code names
    '''
    # handle single values
    if type(column_list) != type([]):
        column_list = [column_list]    
    # get the org_Code lookup
    if org_lkp is None:
        df_org_lkp = dss_org_api(conn=conn).set_index('OrganisationId')['Name']  # this allows us to pull names easily
    # join the columns on
    df_out = df.copy()
    for column in column_list:
        df_out = df_out.join(df_org_lkp, on=column).rename(columns={'Name': column + '_name'})
    return df_out

def sno_col(df, column_list,df_sno_lkp=None, conn=conn_DSS2016UAT()):
    '''Desc: Converts column of SNOMED codes into SNOMED descriptions (TERMs) using DSS SNOMED tables.
    inputs:
    -------
     df : pd.DataFrame
        dataframe with a column of SNOMED codes
    column_list : list
        list of column names with SNOMED codes
    Returns:
    --------
    df : pd.DataFrame
        submitted df with additional columns called column+"_desc" with corresponding SNOMED TERMS
    '''
    # handle single values
    if type(column_list) == type([]):
        column_list = [column_list]
    if df_sno_lkp is None:
        df_sno_lkp = SNO_lkp(conn=conn).set_index('CONCEPT_ID')
    df_out = df.copy()
    for column in column_list:
        print('sno_col: ', column)
        df_out = df_out.join(df_sno_lkp, on=column).rename(columns={'TERM': column + '_desc'})
    return df_out


def icd10_col(df, column_list, fourchar=False, df_icd10_lkp=None, conn=conn_DSS2016UAT()):
    '''Desc: Converts column of ICD10 codes into ICD10 descriptions using DSS ICD10 tables.
    inputs:
    -------
     df : pd.DataFrame
        dataframe with a column of ICD10 codes
    column_list : list
        list of column names with ICD10 codes
    Returns:
    --------
    df : pd.DataFrame
        submitted df with additional columns called column+"_desc" with corresponding ICD10 descriptions
    '''
    if fourchar is True:
        code = 'CODE'
    else:
        code = 'ALT_CODE'
    if df_icd10_lkp is None:
        df_icd10_lkp = ICD10_lkp(conn=conn)[[code, 'ICD10_DESCRIPTION']].set_index(code)
    if type(column_list) != type([]):
        column_list = [column_list]
    df_out = df.copy()
    for column in column_list:
        df_out = (df_out.join(df_icd10_lkp, on=column, how='left')
                        .rename(columns={'ICD10_DESCRIPTION': column + '_desc'}))
    return df_out


'''Ref Data'''
def dss_org_api(conn=conn_DSS2016UAT()):
    '''pulls all current org_codes from the ODS API feed tables'''
    df_dss_org = pd.read_sql('''SELECT [Name]
                              ,[OrganisationId]
                              ,[DateType]
                              ,[StartDate]
                              ,[EndDate]
                              ,[Status]
                              ,[OrganisationRoot]
                              ,[AssigningAuthorityName]
                              ,[LastChangeDate]
                              ,[OrgRecordClass]
                              ,[refOnly]
                              ,[AddrLn1]
                              ,[AddrLn2]
                              ,[AddrLn3]
                              ,[Town]
                              ,[County]
                              ,[PostCode]
                              ,[Country]
                              ,[UPRN]
                              ,[SysStartTime]
                              ,[SysEndTime]
                          FROM [DSS_CORPORATE].[dbo].[ODSAPIOrganisationDetails]
                          WHERE DateType = 'Operational' and SysEndTime = '9999-12-31 23:59:59.9999999'
                          ''', conn)
    return df_dss_org


def ICD10_lkp(, conn=conn_DSS2016UAT()):
    '''Desc: Creates and returns pd.DataFrame of ICD10 codes [CODE] and associated descriptions [ICD10_DESCRIPTION]'''
    ICD10_sql = """SELECT [DSS_KEY]
          ,[CODE]
          ,[ALT_CODE]
          ,[ICD10_DESCRIPTION]
          ,[DESCRIPTIONS_ABBREVIATED]
          ,[ICD10_CHAPTER_HEADING]
          ,[ICD10_CHAPTER_DESCRIPTION]
          ,[ICD10_GROUP_HEADING]
          ,[ICD10_GROUP_DESCRIPTION]
          ,[VERSION]
          ,[DSS_SYSTEM_CREATED_DATE]
      FROM [DSS_CORPORATE].[ICD10].[ICD10_GROUP_CHAPTER_V01]"""

    df_ICD10_lkp = pd.read_sql_query(ICD10_sql, conn)
    return df_ICD10_lkp


def SNO_lkp(conn=conn_DSS2016UAT()):
    '''Desc: Creates and returns pd.DataFrame of SNOMED codes [CONCEPT_ID] and associated descriptions [TERM]
        Due to the nature of the SNOMED table, it's difficult to make a one-to-one mapping. Hence the SQL script '''
    SNO_sql = '''
                WITH MAX_CODE_DATE AS (
                    SELECT 
                        CONCEPT_ID,
                        max([EFFECTIVE_TIME]) AS [EFFECTIVE_TIME]
                    FROM [DSS_CORPORATE].[SNOMED].[SNOMED_CT_RF2_DESCRIPTIONS]
                    WHERE TYPE_ID='900000000000003001' and ACTIVE = 1
                    GROUP BY CONCEPT_ID),
                MAX_ID AS (
                    SELECT 
                        sno.CONCEPT_ID, 
                        MAX(ID) as ID 
                    FROM [DSS_CORPORATE].[SNOMED].[SNOMED_CT_RF2_DESCRIPTIONS] as sno 
                    INNER JOIN MAX_CODE_DATE as mcd
                        on sno.CONCEPT_ID = mcd.CONCEPT_ID 
                        and sno.EFFECTIVE_TIME = mcd.EFFECTIVE_TIME
                    GROUP BY sno.CONCEPT_ID)
                SELECT 
                    DISTINCT sno.CONCEPT_ID, 
                    TERM 
                FROM [DSS_CORPORATE].[SNOMED].[SNOMED_CT_RF2_DESCRIPTIONS] as sno 
                INNER JOIN MAX_ID as maxid
                    on sno.CONCEPT_ID = maxid.CONCEPT_ID and sno.ID = maxid.ID
                ORDER BY CONCEPT_ID
                '''
    df_SNO = pd.read_sql_query(SNO_sql,conn)
    return df_SNO
