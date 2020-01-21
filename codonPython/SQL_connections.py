''' Author(s): Sam Hollings
Desc: this module contains SQL_alchemy engines to connect to commonly used databases'''

from sqlalchemy import create_engine


def conn_dss():
    '''Returns sqlalchemy Engine to connect to the DSS 2008 server (DMEDSS) DSS_CORPORATE database '''
    engine = create_engine('mssql+pyodbc://DMEDSS/DSS_CORPORATE?driver=SQL+Server')
    return engine


def conn_dss2016uat():
    '''Returns sqlalchemy Engine to connect to the DSS 2016 server (UAT) (DSSUAT) DSS_CORPORATE database '''
    conn = create_engine('mssql+pyodbc://DSSUAT/DSS_CORPORATE?driver=SQL+Server')
    return conn


def conn_dummy(path=r''):
    '''connect to the sqlite3 database in memory, or at specified path
    parameters
    ----------
    path : string
        The location and file in which the database for conn_dummy will be stored. Default is memory (RAM)
    '''

    conn_string = 'sqlite://'
    if path != '':
        path = '/' + path

    conn = create_engine(r'{0}{1}'.format(conn_string, path))

    return conn
