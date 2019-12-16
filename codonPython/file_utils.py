import pandas as pd
import os


def file_search(path=".", doctype="csv", like=[""], strict=False):
    """
    This function creates a list of all files of a certain type, satisfying the criteria outlined
    in like = [...] parameter. The function only searches for files in the specified folder
    of the current working directory that is set by the user.

    Parameters
    -----------
    path : string
        Path to a folder in the current working directory
        default = '.', i.e. current working directory folder
    doctype : string
        Document format to search for
        e.g. 'csv' or 'xlsx'
        default = 'csv'
    like : list
        A list of words to filter the file search on
        default = [''], i.e. no filter
    strict : bool
        Set True to search for filenames containing all words from 'like' list (
        default = False

    Returns
    -------
    list

    Examples
    -------
    >>> file_search(doctype = 'md')
    ['README.md', 'CONTRIBUTING.md']

    >>> file_search(doctype = 'md', like = ['READ'])
    ['README.md']

    """

    if not isinstance(path, str):
        raise ValueError("Please input path as a string")
    elif not isinstance(doctype, str):
        raise ValueError("Please input doctype as a string")
    elif not isinstance(like, list):
        raise ValueError("Please input like as a list")
    elif not isinstance(strict, bool):
        raise ValueError("Please input strict as a bool")
    else:
        pass

    list_of_files = []

    if strict is False:
        for file in os.listdir(path):
            if (file.split(".")[-1] == doctype) & (any(x in file for x in like)):
                list_of_files.append(file)
    else:
        for file in os.listdir(path):
            if (file.split(".")[-1] == doctype) & (all(x in file for x in like)):
                list_of_files.append(file)

    return list_of_files


def import_files(
    path=".", doctype="csv", sheet="Sheet1", subdir=False, like=[""], strict=False
):
    """
    This function imports all documents of a given format to a dictionary
    and returns this dictionary, keeping original file names.

    Parameters
    ----------
    path : string
        Path to a folder in the current working directory
        default = '.', i.e. current working directory folder
    doctype : string
        Document format to search for
        e.g. 'csv' or 'xlsx'
        default = 'csv'
    sheet : string
        Sheet name of the xlsx file
        default = 'Sheet1'
    subdir : bool
        True to allow download all files, including the subdirectories
        default = False
    like : list
        A list of words to filter the file search on
        default = [''], i.e. no filter
    strict : bool
        Set True to search for filenames containing all words from 'like' list
        default = False

    Returns
    -------
    out : dict

    Examples
    --------

    '>>> import_files()'

    File Data_AprF_2019 is successfully imported

    File Data_AugF_2019 is successfully imported

    File Data_JulF_2019 is successfully imported

    File Data_JunF_2019_v1 is successfully imported

    File Data_MayF_2019 is successfully imported

    File Data_SepP_2019 is successfully imported

    '>>> import_files(like = ['Aug','Sep'])'

    File Data_AugF_2019 is successfully imported

    File Data_SepP_2019 is successfully imported


    """

    if not isinstance(path, str):
        raise ValueError("Please input path as a string")
    elif not isinstance(doctype, str):
        raise ValueError("Please input doctype as a string")
    elif not isinstance(sheet, str):
        raise ValueError("Please input sheet as a string")
    elif not isinstance(subdir, bool):
        raise ValueError("Please input subdir as a bool")
    elif not isinstance(like, list):
        raise ValueError("Please input like as a list")
    elif not isinstance(strict, bool):
        raise ValueError("Please input strict as a bool")
    else:
        pass

    dict_files = {}
    if subdir is True:

        for r, d, f in os.walk(path):
            for file in f:
                b = any(x in file for x in like)
                if strict is True:
                    b = all(x in file for x in like)
                if (file.split(".")[-1] == doctype) & (b is True):
                    k = file.strip("." + doctype)
                    try:
                        name = os.path.join(r, file)
                        print("\nImporting " + k + "...", end="", flush=True)
                        if doctype == "csv":
                            dict_files[name.strip(".\\").strip(".csv")] = pd.read_csv(
                                name
                            )
                            print("\rFile " + k + " is successfully imported")
                        else:
                            dict_files[
                                name.strip(".\\").strip(".xlsx")
                            ] = pd.read_excel(name, sheet_name=sheet)
                            print("\rFile " + k + " is successfully imported")
                    except Exception as ex:
                        raise (ex)
    else:
        for file in os.listdir(path):
            b = any(x in file for x in like)
            if strict is True:
                b = all(x in file for x in like)

            if (file.split(".")[-1] == doctype) & (b is True):
                k = file.strip("." + doctype)
                try:
                    name = os.path.join(path, file)
                    print("\nImporting " + k + "...", end="", flush=True)
                    if doctype == "csv":
                        dict_files[k] = pd.read_csv(name)
                        print("\rFile " + k + " is successfully imported")
                    else:
                        dict_files[k] = pd.read_excel(name, sheet_name=sheet)
                        print("\rFile " + k + " is successfully imported")
                except Exception as ex:
                    raise (ex)

    return dict_files


def compare(x, y, names=["x", "y"], dups=False, same=False, comment=False):
    """
    This function returns a dictionary with:

        1. Same values between data frames x and y
        2. Values in x, not in y
        3. Values in y, not in x

        (optional):
        (4) Duplicates of x
        (5) Duplicates of y
        (6) Boolean of whether x and y are the same

    Parameters
    ----------
    x : pandas.DataFrame
        DataFrame #1
    y : pandas.DataFrame
        DataFrame #2
    names : list
        a list of user preferred file names
        e.g. ['File1', 'File2']
        default = ['x','y']
    dups : bool
        True to include duplicates check for each file
        default = False
    same : bool
        True to activate. Outputs True if DataFrames are the same
        default = False
    comment : bool
        True to activate. Prints out statistics of the compariosn results
        e.g. number of same valeus, number of duplicates, number of outliers and whether the DataFrames are the same
        default = False

    Returns
    -------
    out : dict

    Examples
    --------

    '>>> c = compare(df1, df2, names = ['df1','df2'], dups = True, same = True, comment =True)'

    There are 133891 same values
    There are 16531 outliers in df1
    There are 20937 outliers in df2
    There are 48704 duplicates in df1
    There are 0 duplicates in df2
    The DataFrames are not the same

    '>>> c = compare(df2, df2, names = ['df2','df2'], dups = True, same = True, comment =True)'

    There are 154444 same values
    There are 0 outliers in df2
    There are 0 outliers in df2
    There are 0 duplicates in df2
    There are 0 duplicates in df2
    The DataFrames are the same
    """

    if not isinstance(x, pd.DataFrame):
        raise ValueError("Please input x as a pandas.DataFrame")
    elif not isinstance(y, pd.DataFrame):
        raise ValueError("Please input y as a pandas.DataFrame")
    elif not isinstance(names, list):
        raise ValueError("Please input names as a list")
    elif not isinstance(dups, bool):
        raise ValueError("Please input dups as a bool")
    elif not isinstance(same, bool):
        raise ValueError("Please input same as a bool")
    elif not isinstance(comment, bool):
        raise ValueError("Please input comment as a bool")

    dict_temp = {}

    try:
        dict_temp["same_values"] = pd.merge(
            x.drop_duplicates(), y.drop_duplicates(), how="inner"
        )
    except Exception as ex:
        raise (ex)
    try:
        dict_temp[names[0] + "_not_" + names[1]] = pd.concat(
            [x, dict_temp["same_values"]], ignore_index=True
        ).drop_duplicates(keep=False)
        dict_temp[names[1] + "_not_" + names[0]] = pd.concat(
            [y, dict_temp["same_values"]], ignore_index=True
        ).drop_duplicates(keep=False)
    except Exception as ex:
        raise (ex)

    if dups is True:
        try:
            dict_temp[names[0] + "_dups"] = x[x.duplicated()]
            dict_temp[names[1] + "_dups"] = y[y.duplicated()]
        except Exception as ex:
            raise (ex)
    if same is True:
        try:
            if (x.shape == y.shape) & (x.shape == dict_temp["same_values"].shape):
                dict_temp["Same"] = True
            else:
                dict_temp["Same"] = False
        except Exception as ex:
            raise (ex)
    try:
        if comment is True:
            print(
                "\nThere are " + str(dict_temp["same_values"].shape[0]) + " same values"
            )
            print(
                "There are "
                + str(dict_temp[names[0] + "_not_" + names[1]].shape[0])
                + " outliers in "
                + str(names[0])
            )
            print(
                "There are "
                + str(dict_temp[names[1] + "_not_" + names[0]].shape[0])
                + " outliers in "
                + str(names[1])
            )
            if dups is True:
                print(
                    "There are "
                    + str(dict_temp[names[0] + "_dups"].shape[0])
                    + " duplicates in "
                    + names[0]
                )
                print(
                    "There are "
                    + str(dict_temp[names[1] + "_dups"].shape[0])
                    + " duplicates in "
                    + names[1]
                )
            if same is True:
                if dict_temp["Same"] is True:
                    s = "the same"
                else:
                    s = "not the same"
                print("DataFrames are " + s)
    except Exception as ex:
        raise (ex)

    return dict_temp
