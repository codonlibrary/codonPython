import pyodbc

# pyodbc connection
cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=GLDMSRV009;'
                      'Database=DSS_CORPORATE;'
                      'Trusted_Connection=yes;')
                      
try:
    # execute sql through the pyodbc cursor
    cursor = cnxn.cursor()
    cursor.execute('''BULK INSERT [dbo].[AD_Users2]
FROM 'C:\\Users\wasw1\\Desktop\Python_Scripts\\AD_Users.txt' WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR='\\t',
    ROWTERMINATOR='\\n'
    );
    ''')
except TypeError as error:
    print(error)

# commit transaction
cnxn.commit()

print("Inserted Successfully")