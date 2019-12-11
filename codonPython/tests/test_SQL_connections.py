'''test script for SQL_connections
- test the connections can run a dummy script (SELECT 1 as [Code], 'test' as [Name])'''
import pandas as pd
import unittest
import common_python.SQL_connections as conn 

class Test_connections(unittest.TestCase):
	# Test the SQL database connections
	def setUp(self):
		self.conn = {'MH': conn.conn_MH()}
		self.conn['HES'] = conn.conn_HES()
		self.conn['DSS'] = conn.conn_DSS()
		self.conn['DSS2016UAT'] = conn.conn_DSS2016UAT()

	def test_SELECT1(self):
		for conn_name, conn in self.conn.items():
			# Check connection can run simple SQL script
			with self.subTest(conn=conn_name):
				self.assertEqual(pd.read_sql("""SELECT 1 as [Code], 'Test' as [Name]""", conn).iloc[0,0],
								 pd.DataFrame([{'Code': 1, 'Name' : 'Test'}]).iloc[0,0])

if __name__ == '__main__':
	unittest.main()
