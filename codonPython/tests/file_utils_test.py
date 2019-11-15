from codonPython.file_utils import compare
import numpy as np
import pytest
import pandas as pd

df1 = pd.DataFrame({
'A' : [1,5,6,1,8,5,9],
'B' : [2,8,5,2,21,3,5],
'C' : [3,4,5,3,1,5,9],
'D' : [2,8,5,2,4,6,2],
'E' : [1,2,6,1,3,5,5]})

df2 = pd.DataFrame({
'A' : [1,5,6,1,9,5,9],
'B' : [2,9,5,2,21,3,5],
'C' : [3,4,5,3,1,35,9],
'D' : [2,8,7,2,4,6,2],
'E' : [1,2,46,1,3,8,5]})

dict_test = {'same_values': pd.DataFrame(np.array([[1,  2,  3,  2,  1],[9,  5,  9,  2,  5]]),
                                    columns = ['A','B','C','D','E']), 
         'df1_not_df2': pd.DataFrame(np.array([[5,8,4,8,2],
                                             [6,5,5,5,6],
                                             [8,21,1,4,3],
                                             [5,3,5,6,5]]), 
                                columns = ['A','B','C','D','E']), 
         'df2_not_df1': pd.DataFrame(np.array([[5,   9,   4,  8,   2],
                         [6,   5,   5,  7,  46],
                         [9,  21,   1,  4,   3],
                         [5,   3,  35,  6,   8]]),
                columns = ['A','B','C','D','E']), 
        'df1_dups' : pd.DataFrame(np.array([[1,  2,  3,  2,  1]]),
                                  columns = ['A','B','C','D','E']), 
        'df2_dups':   pd.DataFrame(np.array([[1,  2,  3,  2,  1]]),
                                   columns = ['A','B','C','D','E']),  
        'Same': False}

@pytest.mark.parametrize("x, y, names = ['x','y'],expected", [
    (
        pd.DataFrame({
            'A' : [1,5,6,1,8,5,9],
            'B' : [2,8,5,2,21,3,5],
            'C' : [3,4,5,3,1,5,9],
            'D' : [2,8,5,2,4,6,2],
            'E' : [1,2,6,1,3,5,5]}),
    
        pd.DataFrame({
            'A' : [1,5,6,1,9,5,9],
            'B' : [2,9,5,2,21,3,5],
            'C' : [3,4,5,3,1,35,9],
            'D' : [2,8,7,2,4,6,2],
            'E' : [1,2,46,1,3,8,5]}),
        
        True,
        
        True,
        
        False
    
    ),
    (
        dict_test
    )])

def test_compare_BAU(x, y, expected):
    dict_test_1 = compare(x, y, names = ['df1','df2'], dups = True, same = True)
    for i in expected.keys():
        if i == 'Same':
            assert dict_test_1[i] == expected[i]
        else: 
            for j in expected[i]:
                list_test_1 = list(dict_test_1[i][j])
                list_exp = list(expected[i][j])
                assert list_test_1 == list_exp
