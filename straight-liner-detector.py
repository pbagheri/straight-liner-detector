# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:26:07 2018

@author: payam.bagheri
"""

import pandas as pd
from os import path
from difflib import SequenceMatcher


dir_path = path.dirname(path.dirname(path.abspath(__file__)))
print(dir_path)
filename = str(dir_path) + '\\0_input_data\\data.csv'
print(filename)


data_orig = pd.read_csv(filename, encoding = "ISO-8859-1",low_memory=False)
data = data_orig.copy()
varnam = list(data.columns)

varnam = [x for x in varnam if any(char.isdigit() for char in x)]

# Checks if a string is composed of only numerical characters:
def num_check(s):
    try:
        if type(int(s)) == int:
            return True
    except ValueError:
        return False


# takes two strings and returns true if the difference between them is only numerical characters,
# otherweise returs false
def diff_finder(s1,s2):
    cc = 0
    ml = min(len(s1),len(s2))
    while s1[cc] == s2[cc]:
        cc += 1
        if cc >= ml:
            break
    st1 = s1[cc:]
    st2 = s2[cc:]
    dd1 = 0
    i = 0
    while (i <len(st1) and num_check(st1[i])):
        dd1 += 1
        i += 1        
    dd2 = 0
    j = 0
    while (j <len(st2) and num_check(st2[j])):
        dd2 += 1
        j += 1        
    str1 = s1[cc + dd1:]
    str2 = s2[cc + dd2:]
    st1_r=str1[::-1]
    st2_r=str2[::-1]
    dd = 0
    mlr = min(len(st1_r),len(st2_r))
    if (len(st1_r)>0 and len(st2_r)>0):
        while st1_r[dd] == st2_r[dd]:
            dd += 1
            if dd >= mlr:
                break
    stor1 = s1[cc:len(s1)-dd]
    stor2 = s2[cc:len(s2)-dd]
    c = ''.join(stor1)
    d = ''.join(stor2)
     
    try:
        diff = int(d)-int(c)
    except ValueError:
        diff = 2
    if diff == 1:
        return True
    else:
        return False

# Finds the common numerical parts 
def full_com(s1,s2):
    l1 = list(s1)
    l2 = list(s2)
    i = 0
    com = []
    while i < min(len(l1),len(l2)):
        if l1[i] == l2[i]:
            com.append(l1[i])
            i += 1
        else:
            break
    left = ''.join(com)
    s1r = s1[::-1]
    s2r = s2[::-1]
    l1r = list(s1r)
    l2r = list(s2r)
    i = 0
    comr = []
    while i < min(len(l1r),len(l2r)):
        if l1r[i] == l2r[i]:
            comr.append(l1r[i])
            i += 1
        else:
            break
    rite = ''.join(comr)
    rite = rite[::-1]
    full = left + rite
    return full
 

  
"""    
diff_finder('sys_pagetime_19.81','sys_pagetime_19.82')
diff_finder('sys_pagetime_c19_r1','sys_pagetime_c20_r1')
diff_finder('sys_pagetime_c19','sys_pagetime_c20')
diff_finder('sys_pagetime_c8','sys_pagetime_c9')
diff_finder('sys_pagetime_c0','sys_pagetime_c1')
diff_finder('sys_pagetime_c1','sys_pagetime_c2')
diff_finder('sys_pagetime_c10','sys_pagetime_c11')
diff_finder('sys_pagetime_c0_','sys_pagetime_c1_')
diff_finder('sys_pagetime_c0','sys_pagetime_c2')
diff_finder('sys_pagetime_c0_r1','sys_pagetime_c2_r1')
diff_finder('sys_pagetime_17','sys_pagetime_1')
diff_finder('sys_pagetime_17','abc_9')
diff_finder('ACBC_ChoiceTask10_shown','ACBC_ChoiceTask10')
diff_finder('sys_pagetime_48','sys_pagetime_58')
"""

def list_elem_drop(ls,k):   
    d = 0
    nn = ls[0]
    while nn != k:
        d += 1
        nn = ls[d]
    del ls[d] 


def com_st(s1,s2):
    match = SequenceMatcher(None, s1,s2).find_longest_match(0, len(s1), 0, len(s2))
    c = s1[match.a: match.a + match.size]
    return c

com_st('PackGuidedSevenHeaven1.1', 'PackGuidedSevenHeaven2.1')



# stores sets of consecutive var names in a dataframe with a distinct index for each set.
simnames = pd.DataFrame(columns=['A','B'])
c=0
for x in range(len(varnam)-1):
    if diff_finder(varnam[x],varnam[x+1]):
        if varnam[x] not in list(simnames['B']):
            simnames = simnames.append({'A':c, 'B':varnam[x]}, ignore_index=True)
        if varnam[x+1] not in list(simnames['B']):
            simnames = simnames.append({'A':c, 'B':varnam[x+1]}, ignore_index=True)
    else:
        c += 1

     
for i in list(simnames['B']):
    if i in varnam:
        varnam.remove(i)
rem_names = varnam
    
col_nam = []
i=0
while i < len(rem_names):
    a = rem_names[i]
    kk = 0
    j = i + 1    
    while j < len(rem_names):
        b = rem_names[j]
        if diff_finder(a,b):
            if (kk == 0 and a not in col_nam):
                col_nam.append(a)
                kk = 1
            col_nam.append(b)
            k = a
            a = b
            list_elem_drop(rem_names,k)
            i -= 1
        j += 1        
    i += 1
    
c += 1
for x in range(len(col_nam)-1):
    if diff_finder(col_nam[x],col_nam[x+1]):
        if col_nam[x] not in list(simnames['B']):
            simnames = simnames.append({'A':c, 'B':col_nam[x]}, ignore_index=True)
        if col_nam[x+1] not in list(simnames['B']):
            simnames = simnames.append({'A':c, 'B':col_nam[x+1]}, ignore_index=True)
    else:
        c += 1

        
bare_names = []        
d = -1
for x in simnames['A'].unique():
    d += 1
    s1 = simnames['B'].iloc[d]
    l = list(simnames['B'][simnames['A']==x].index)
    for y in l[0:-1]:
        s1 = full_com(s1,simnames['B'].iloc[y+1])
        d += 1
    bare_names.append(s1)


c= 0    
for i in simnames['A'].unique():
    vrnc_name = bare_names[c]+'-variance'
    data_orig[vrnc_name] = data[list(simnames['B'][simnames['A']==i])].var(axis=1, skipna=None)
    c += 1

c= 0    
for i in simnames['A'].unique():
    vrnc_name = bare_names[c]+'-variance'
    ifs = [1 if x==0 else 0 for x in data_orig[vrnc_name]]
    ifs_name = bare_names[c]+'-ind'
    data_orig[ifs_name] = ifs
    c += 1
    
c= 0    
for i in simnames['A'].unique():
    vrnc_name = bare_names[c]+'-variance'
    q1 = data_orig[vrnc_name].quantile(q=0.25, interpolation='linear')
    q3 = data_orig[vrnc_name].quantile(q=0.75, interpolation='linear')
    iqr = q3-q1
    outs = [1 if (x < (q1-1.5*iqr) or x > (q3+1.5*iqr)) else 0 for x in data_orig[vrnc_name]]
    outs_name = bare_names[c]+'-out'
    data_orig[outs_name] = outs
    c += 1


'''
col_nam
col_nam = pd.Series(col_nam)
col_nam.to_csv(dir_path + '\\0_output\\col_nam.csv', index=False)
'''
    
data_orig.to_excel(dir_path + '\\0_output\\new_data.xlsx', index=False, header=True)
simnames.to_csv(dir_path + '\\0_output\\simnames.csv', index=False)

#bare_names = pd.DataFrame(bare_names)
#bare_names.to_csv(dir_path + '\\0_output\\barenames.csv', index=False)



