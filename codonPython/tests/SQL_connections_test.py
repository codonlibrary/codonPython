'''test script for SQL_connections
- test the connections can run a dummy script (SELECT 1 as [Code], 'test' as [Name])'''
from codonPython import SQL_connections
import pandas as pd
import pytest
import codonPython.SQL_connections as conn

@pytest.mark.parametrize("connection", 
			 [conn.conn_DSS(),
			  conn.conn_DSS2016UAT()
			 ])
def test_SELECT1(connection):
	sql = """SELECT 1 as [Code], 'Test' as [Name]"""
	result = pd.read_sql("""SELECT 1 as [Code], 'Test' as [Name]""", connection).iloc[0,0]
	expected = pd.DataFrame([{'Code': 1, 'Name' : 'Test'}]).iloc[0,0]
	assert result == expected
