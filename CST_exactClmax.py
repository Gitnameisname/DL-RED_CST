# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 15:34:52 2020

@author: CK_DL2
"""

"""
Info - Kor
====================
본 코드는 에어포일 데이터베이스의 Cl,max와 AoA of Cl,max 값을 보다 정밀하게 찾아냅니다.

Info - Eng
====================
This code finds Cl,max and AoA of Cl,max's more exact values 
"""

import numpy as np
import os
import sys
import time

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

direct_work=os.getcwd()
direct_code=os.path.dirname(os.path.realpath(__file__))
sys.path.append(direct_code)

import CST_ReadDB as RDB
import CST_AF
import CST_writeDB as wDB
import CST_RunXfoil as RunXfoil
import CST_Dataset as Dataset
import CST_Rinput as Rin
import CST_message as msg
import CST_Log as Log

name_inputfolder = 'Input'
name_inputfile = 'input.txt'


"""
Airfoil DB를 읽어들입니다.
"""

def UpdateDB_Clmax(loop, DBname_AFDB, DBname_AFDB_Enhanced):

    wDB.CSTDB_gen(DBname_AFDB_Enhanced)
    
    time_start = time.time()
    
    var, val = Rin.Rinput(name_inputfolder, name_inputfile, 2)
    no_input = int(val[2])
    no_output = int(val[3])
    
    var, val = Rin.Rinput(name_inputfolder, name_inputfile, 4)
    no_proc = int(val[0])
    no_proc_fix = int(val[0])
    AoA_cut = int(val[1])
    
    no_proc_available = cpu_count()
    
    index_Cl_max = 12
    index_AoA_Cl_max = 13
    indexes = [index_Cl_max, index_AoA_Cl_max]
    
    index_Re = 8
    index_Mach = 9
    
    step_AoA = 0.1
    
    if no_proc >= no_proc_available:
        msg.debuginfo('Exceeded the number of available processors')
        msg.debuginfo(str('User input: {}, Available: {}'.format(no_proc,no_proc_available)))
        msg.debuginfo(str('Number of Process was changed: {} >> {}'.format(no_proc, no_proc-2)))
        no_proc = no_proc_available - 2
    
    try:
        AFDB = RDB.Read(DBname_AFDB)
        split_AFDB = np.array_split(AFDB, no_proc)
        
        i = 0
        
        size_split_AFDB = []
        for i in range(no_proc):
            size_split_AFDB.append(np.shape(split_AFDB[i])[0])
            name_split_AFDB = 'split_AFDB'+str(i)
            vars()[name_split_AFDB] = split_AFDB[i]
            
            if size_split_AFDB[i] != size_split_AFDB[i-1]:
                last_max_DB = i
        
        
        i = 0
    
        for i in range(no_proc):
            name_split_AFDB_Enhanced = 'split_AFDB_Enhanced'+str(i)
            vars()[name_split_AFDB_Enhanced] = np.zeros([0, no_input + no_output])
            
        msg.debuginfo(str('Size of the splited CST airfoil DB: {}'.format(size_split_AFDB)))
        
        
        # Seperated DB can have differente size #
        # for prevent the error, record max/min size of split DB#
        max_iter = max(size_split_AFDB)
        
        # max_iter = 2 # for test
        
        min_iter = min(size_split_AFDB)
            
        msg.debuginfo(None)
        msg.debuginfo(str('XFOIL Analysis Start'))
        
        msg.debuginfo('====================')
        line=0 # no_Airfoil at sepertated configuration DB
        
        while line < max_iter:
                
            if line > min_iter - 1:
                no_proc = last_max_DB
            
            progress=('Progress: '+str(line+1)+'/'+str(max_iter))
            sys.stdout.write('\r'+progress)    
            
            try:
                
                i = 0
                target_AoA = []
                target_Re = []
                target_Mach = []
                for i in range(no_proc):
                    N1=0.5
                    N2=1.0
                    
                    AF_case = split_AFDB[i][line, 0:8]
                    target_AoA.append(split_AFDB[i][line, index_AoA_Cl_max])
                    target_Re.append(split_AFDB[i][line, index_Re])
                    target_Mach.append(split_AFDB[i][line, index_Mach])
                
                    AF = CST_AF.CST_shape(N1,N2,AF_case[0:4],AF_case[4:8])
                    AF.airfoil_coor(i,line)
                    
                pool = ThreadPool(no_proc)
                
                i = 0
                
                for i in range(no_proc):
                    pool.apply_async(RunXfoil.runXfoil_custom, args= (i, 200, target_AoA[i] -1 , target_AoA[i] + 1, step_AoA, target_Re[i], target_Mach[i]))
                    
                pool.close()
                pool.join()
                
                i = 0
                
                for i in range(no_proc):
                    name_split_AFDB_Enhanced = 'split_AFDB_Enhanced'+str(i)
                    updated_data = Dataset.Update_Clmax(i, loop, split_AFDB[i][line, :], indexes, AoA_cut + 1 - step_AoA)
                    
                    if len(updated_data) > 0:
                        vars()[name_split_AFDB_Enhanced] = np.append(vars()[name_split_AFDB_Enhanced],np.array([updated_data]),0)
                
                line += 1
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                message1 = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
                Log.log(message1)
                message2 = str('Error Occured in progress: {}/{}'.format(line+1,max_iter))
                msg.debuginfo(message2)
                msg.debuginfo(progress)
                line = max_iter
                
        i = 0
        Full_airfoilDB_Enhanced = np.zeros([0,no_input+no_output])
        for i in range(no_proc_fix):
            name_split_AFDB_Enhanced = 'split_AFDB_Enhanced'+str(i)
            Full_airfoilDB_Enhanced = np.append(Full_airfoilDB_Enhanced, vars()[name_split_AFDB_Enhanced],0)
    
        print('\n')
        msg.debuginfo('====================')
        msg.debuginfo('XFOIL Analysis Ended')
        time_run = time.time()-time_start
        msg.debuginfo(str('Run Time: {:.2f} min, {:.2f} hr'.format(time_run/60,time_run/3600)))
        wDB.CSTDB(DBname_AFDB_Enhanced,Full_airfoilDB_Enhanced)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)
    
if __name__ == '__main__':
    

    loop = 1
    DBname_AFDB = "CST Airfoil DB sorted " + str(loop) + ".txt"
    DBname_AFDB_Enhanced = "CST Airfoil DB Enhaced "+ str(loop) + ".txt"

    UpdateDB_Clmax(loop, DBname_AFDB, DBname_AFDB_Enhanced)
