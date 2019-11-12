import pandas as pd
import os
import datetime
from calendar import monthrange

def file_search(path = '.', doctype = 'csv', like = [''], strict = False):
    """
    Args:
        path: Path to the folder (default = '.')
        doctype: Document format to search for (e,g, '.csv' or '.xlsx', default = 'csv')
        like: A list of words to filter the file search on (default = [''], i.e. no filter)
        strict: Set True to search for filenames containing all words from 'like' list (default = False) 
        
    This function creates a list of all files of a certain type, satisfying the criteria outlined
    in like = [...] parameter.
    """
    
    list_of_files = []
    
    if strict == False:
        for file in os.listdir(path):
            if (file.split('.')[-1] == doctype) & (any(x in file for x in like)):
                list_of_files.append(file) 
    else:
        for file in os.listdir(path):
            if (file.split('.')[-1] == doctype) & (all(x in file for x in like)):
                list_of_files.append(file) 

            
    return list_of_files
        
    

def import_files(path = '.', doctype = 'csv', sheet = 'Sheet1', subdir = False, like = [''], strict = False):
    """
    Args:
        path: Path to the folder (default = '.')
        doctype: Document format ('csv' or 'xlsx', default = 'csv')
        subdir: True to allow download all files, including the subdirectories (default = False)
        like: A list of words to filter the file search on (default = [''], i.e. no filter)
        strict: Set True to search for filenames containing all words from'like' list (default = False) 

        
    This function imports all documents of a given format to a dictionary
    and returns this dictionary, keeping original file names.
    """  
    dict_files = {}
    if subdir == True:
        
        for r, d, f in os.walk(path):
            for file in f:
                b = any(x in file for x in like)
                if strict == True:
                    b = all(x in file for x in like)
                if (file.split('.')[-1] == doctype) & (b == True):
                    k = file.strip('.' + doctype)
                    try:
                        name = os.path.join(r,file)
                        print('\nImporting ' + k + '...', end = "", flush = True)
                        if doctype == 'csv':
                            dict_files[name.strip('.\\').strip('.csv')] = pd.read_csv(name)
                            print('\rFile ' + k + ' is successfully imported')
                        else:
                            dict_files[name.strip('.\\').strip('.xlsx')] = pd.read_excel(name, sheet_name = sheet)
                            print('\rFile ' + k + ' is successfully imported')
                    except:
                        print('Unable to read ' + k + ' file')
    else:
        for file in os.listdir(path):
            b = any(x in file for x in like)
            if strict == True:
                b = all(x in file for x in like)

            if (file.split('.')[-1] == doctype) & (b == True):
                k = file.strip('.' + doctype)
                try:
                    name = os.path.join(path,file)
                    print('\nImporting ' + k + '...', end = "", flush = True)
                    if doctype == 'csv':
                        dict_files[k] = pd.read_csv(name)
                        print('\rFile ' + k + ' is successfully imported')
                    else:
                        dict_files[k] = pd.read_excel(name, sheet_name = sheet)
                        print('\rFile ' + k + ' is successfully imported')
                except:
                    print('Unable to read ' + k + ' file')
    
    return dict_files

def compare(x, y, names, dups = False, same = False):
    """
    Args:
        x: DataFrame #1
        y: DataFrame #2
        names: a list of user preferred file names, e.g. ['File1', 'File2']
        dups: True to include duplicates check for each file (default = False)
        same: True to activate. Outputs True is dfs are the same (default = False)
        
    This function returns a dictionary with:
        
        1. Same values between data frames x and y
        2. Value in x, not in y
        3. Value in y, not in x
        
        (optional):
        (4) Duplicates of x
        (5) Duplicates of y
    """
    dict_temp = {}
    dict_temp['same_values'] = pd.merge(x,y, how = 'inner')
    dict_temp[names[0] + '_not_' + names[1]] = pd.concat([x,dict_temp['same_values']], ignore_index = True).drop_duplicates(keep = False)
    dict_temp[names[1] + '_not_' + names[0]] = pd.concat([y,dict_temp['same_values']], ignore_index = True).drop_duplicates(keep = False)
    if dups == True:
        dict_temp[names[0] + '_dups'] = x[x.duplicated() == True]    
        dict_temp[names[1] + '_dups'] = y[y.duplicated() == True]
    if same == True:
        if (x.shape == y.shape) & (x.shape == dict_temp['same_values'].shape):
            dict_temp['Same'] = True
        else:
            dict_temp['Same'] = False
    return dict_temp

def publication_date(date = datetime.datetime.now()):
    """
    This function returns the publication date for the current month for MHT,
    which is the second Thursday.
    """
    
    year = date.year
    month = date.month
    weekday = date.weekday()
    
    days = monthrange(year,month)[1]
    
    count = 0
    
    for i in range(1,days+1):
        weekday = datetime.datetime(year,month,i).weekday()
        if weekday == 3:
            count += 1
        if count == 2:
            #print('This month publication is on ' + str(i) + '/' + str(month) + '/' + str(year))
            break
    return str(i) + '/' + str(month) + '/' + str(year)