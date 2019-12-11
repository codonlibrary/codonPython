''' Author(s): Sam Hollings
Desc: this module contains SQL_alchemy engines to connect to commonly used databases'''

from sqlalchemy import create_engine

def conn_DSS():
    '''Returns sqlalchemy Engine to connect to the DSS 2008 server (DMEDSS) DSS_CORPORATE database '''
    engine = create_engine('mssql+pyodbc://DMEDSS/DSS_CORPORATE?driver=SQL+Server')
    return engine
    
def conn_DSS2016UAT():
    '''Returns sqlalchemy Engine to connect to the DSS 2016 server (UAT) (DSSUAT) DSS_CORPORATE database '''
    conn = create_engine('mssql+pyodbc://DSSUAT/DSS_CORPORATE?driver=SQL+Server')
    return conn
