import pyodbc 

# pyodbc connection
cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=GLDMSRV009;'
                      'Database=DSS_CORPORATE;'
                      'Trusted_Connection=yes;')
					  
					  
# instantiate cursor
cursor = cnxn.cursor()

# sql command string
sql = """SELECT * FROM [DSS_CORPORATE].[dbo].[AD_Users2] WHERE [Pre_Windows_2000_Logon_Name] LIKE 'W%'"""

# execute sql
cursor.execute(sql)

# display rows held in cursor (no commit as no changes in sql database in this transaction)
for row in cursor:
    print(row)
