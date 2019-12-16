import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


def tableFromSql(
    server: str,
    database: str,
    table_name: str,
    user: str = "",
    password: str = "",
    schema: str = None,
    index_col: str = None,
    coerce_float: bool = True,
    parse_dates: list = None,
    columns: list = None,
    chunksize: int = None,
):
    """
    Returns a SQL table in a DataFrame.

    Convert a table stored in SQL Server 2016 into a pandas dataframe.
    Uses sqlalchemy and pandas.

    Parameters
    ----------
    server : string
        Name of the SQL server
    database : string
        Name of the SQL database
    user : string, default: ""
        If verification is required, name of the user
    password : string, default: ""
        If verification is required, password of the user
    table_name : string
        Name of SQL table in database.
    schema : string, default : None
        Name of SQL schema in database to query (if database flavor supports this). Uses
        default schema if None (default).
    index_col : string or list of strings, default : None
        Column(s) to set as index(MultiIndex).
    coerce_float : boolean, default : True
        Attempts to convert values of non-string, non-numeric objects (like decimal.Decimal)
        to floating point. Can result in loss of Precision.
    parse_dates : list or dict, default : None
        - List of column names to parse as dates.
        - Dict of {column_name: format string} where format string is strftime compatible in
        case of parsing string times or is one of (D, s, ns, ms, us) in case of parsing
        integer timestamps.
        - Dict of {column_name: arg dict}, where the arg dict corresponds to the keyword
        arguments of pandas.to_datetime() Especially useful with databases without native
        Datetime support, such as SQLite.
    columns : list, default : None
        List of column names to select from SQL table
    chunksize : int, default : None
        If specified, returns an iterator where chunksize is the number of rows to include
        in each chunk.

    Returns
    ----------
    pd.DataFrame
        Dataframe of the table requested from sql server

    Examples
    ---------
    # >>> tableFromSql("myServer2", "myDatabase2", "myTable2")
    # pd.DataFrame
    # >>> tableFromSql("myServer", "myDatabase", "myTable", schema="specialSchema", columns=["col_1", "col_3"])
    # pd.DataFrame
    """

    try:
        uri = "mssql+pyodbc://{}:{}@{}/{}?driver=SQL Server Native Client 11.0".format(
            user, password, server, database
        )
        engine = create_engine(uri)
        return pd.read_sql_table(
            table_name,
            engine,
            schema=schema,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            columns=columns,
            chunksize=chunksize,
        )
    except Exception as error:
        raise error
