'''test script for SQL_connections
- test the connections can run a dummy script (SELECT 1 as [Code], 'test' as [Name])'''
import pandas as pd
import pytest
import codonPython.SQL_connections as conn


@pytest.mark.parametrize("connection",
                         [conn.conn_dummy(),
                          conn.conn_dummy('test.db')
                          ])
def test_select1(connection):
    result = pd.read_sql("""SELECT 1 as [Code], 'Test' as [Name]""", connection).iloc[0, 0]
    expected = pd.DataFrame([{'Code': 1, 'Name': 'Test'}]).iloc[0, 0]
    assert result == expected
