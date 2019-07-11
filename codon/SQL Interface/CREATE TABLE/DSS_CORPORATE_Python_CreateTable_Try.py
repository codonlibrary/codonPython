import pyodbc

# pyodbc connection
cnxn = pyodbc.connect("""Driver={SQL Server};
                      Server=GLDMSRV009;
                      Database=DSS_CORPORATE;
                      Trusted_Connection=yes;""")
                    #   UID=USER;
                    #   PWD=PASSWORD)

# SQL query to execute
sql = """
CREATE TABLE [dbo].[AD_Users2](
    [Name] [nvarchar](50) NOT NULL,
    [Pre_Windows_2000_Logon_Name] [nvarchar](50) NOT NULL,
    [E_Mail_Address] [nvarchar](50) NOT NULL
    )
"""

try:
    # Execute sql
    cursor = cnxn.cursor()
    cursor.execute(sql)
except TypeError as error:
    print(error)

# Commit the transaction to 'save' the changes, then close the connection
cnxn.commit()
cnxn.close()


