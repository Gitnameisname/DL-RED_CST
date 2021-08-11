# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 12:43:06 2018

@author: cck18
"""

"""
Info
====
Assort Data
Analyzed
Not Analyzed
"""

import os
import sys
import numpy as np

workdirect=os.getcwd()
direct_code=os.path.dirname(os.path.realpath('__file__'))
direct_DB=os.path.join(direct_code,"DB")
direct_input = os.path.join(direct_code,'Input')

sys.path.append(direct_code)

import CST_ReadDB as ReadDB
import CST_Rinput as Rin

def run(DBname_Answer, DBname_Predict, DBname_Additional_pre):
    
    AddDB=ReadDB.Read(DBname_Additional_pre)
    AnsDB=ReadDB.Read(DBname_Answer)
    PrdDB=ReadDB.Read(DBname_Predict)
    
    var, val = Rin.Rinput(direct_input,'input.txt',2) # 3 Hyperparameters of ANN
    no_output = int(val[3])

    if np.shape(AddDB)[0] == np.shape(AnsDB)[0]:
        print('All data was Analyzed')
        return AddDB, PrdDB, AnsDB
    else:
        i=0
        delete_no = 0
        ## DB identical ##
        tester = 0
        while i < np.shape(AddDB)[0]:
            try:
                if all(AddDB[i][0:no_output] == PrdDB[i][0:no_output]):
                    tester += 1
                    i=i+1
                else:
                    delete_no +=1
                    tester += 1
                    PrdDB=np.delete(PrdDB,i,0)   
                    AnsDB=np.delete(AnsDB,i,0)
            except:
                print('tester: {} '.format(tester))
                print('Shape of Add DB: {}'.format(np.shape(AddDB)))
                print('Shape of Ans DB: {}'.format(np.shape(AnsDB)))
                print('Shape of Prd DB: {}'.format(np.shape(PrdDB)))
                print('i: {}'.format(i))
                i = np.shape(AddDB)[0]

        if np.shape(PrdDB)[0] > np.shape(AddDB)[0]:
            PrdDB=np.delete(PrdDB,i,0)   
            AnsDB=np.delete(AnsDB,i,0)
        
        return AddDB, PrdDB, AnsDB

if __name__=="__main__":
    AddDB2, PrdDB2, AnsDB2 = run(1,8)