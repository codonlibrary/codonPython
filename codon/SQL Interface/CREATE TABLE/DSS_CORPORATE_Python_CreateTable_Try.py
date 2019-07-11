import pyodbc

# pyodbc connection
cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=GLDMSRV009;'
                      'Database=DSS_CORPORATE;'
                      'Trusted_Connection=yes;')

try:
    # Edit the SQL query to align to your table, schema and field constraints
    cursor = cnxn.cursor()
    cursor.execute('''CREATE TABLE [dbo].[AD_Users2](
    [Name] [nvarchar](50) NOT NULL,
    [Pre_Windows_2000_Logon_Name] [nvarchar](50) NOT NULL,
    [E_Mail_Address] [nvarchar](50) NOT NULL
    )
    ''')
except TypeError as error:
    print(error)

# Commit the transaction to 'save' the changes
cnxn.commit()
cnxn.close()


