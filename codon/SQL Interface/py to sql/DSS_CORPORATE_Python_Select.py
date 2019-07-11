import pyodbc

# pyodbc connection
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=GLDMSRV009;"
    "Database=DSS_CORPORATE;"
    "Trusted_Connection=yes;"
)

# instantiate cursor
cur = conn.cursor()

# sql command string
sql = """SELECT * FROM [DSS_CORPORATE].[dbo].[AD_Users2] WHERE [Pre_Windows_2000_Logon_Name] LIKE 'W%'"""

# execute sql
cur.execute(sql)

# display rows held in cursor (no commit as no changes in sql database in this transaction)
for row in cur:
    print(row)
