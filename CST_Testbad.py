# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:56:47 2020

@author: CK_DL2
"""
import numpy as np
from sys import exc_info, stdout

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import CST_message as msg
import CST_Log as Log
import CST_writeDB as wDB
import CST_Rinput as Rin
import CST_AF
import CST_ReadDB as ReadDB
import CST_RunXfoil
import CST_Dataset as AFdataset
import CST_AF as AF



def check_thickness(wl, wu):
    dz = 0.
    N = 200
    airfoil = AF.CST_shape(0.5, 1.0, wl, wu, dz, N)
    coord = airfoil.airfoil_coor()

    thick = []
    
    airfoil2 = AF.CST_shape_preproc(0.5, 1.0, wl, wu, dz, N)
    angle, decision = airfoil2.airfoil_coor()
    
    j = 0
    for j in range(99):
        thick.append(coord[1][j+1]-coord[1][199-j])
        
    thick_max = max(thick)
   
    if thick_max > 0.03 and decision == 1:
    #    airfoil.plotting()
        return thick_max
    
    else:
        return []
        
    

if __name__ == "__main__":
    loop = 1

    filename_Error = 'CST Error DB ' + str(loop) + '.txt'
    filename_Answer = 'CST Answer DB ' + str(loop) + '.txt'
    
    DB_Error = ReadDB.Read(filename_Error)
    DB_Answer = ReadDB.Read(filename_Answer)
    
    # ---------------------- Thickness Check -------------------------------- #
    list_maxThickness = []
    list_configDB_filtered = []
    list_index = []
    
    DB_config = DB_Answer[:,0:8]
    
    no_proc = 10
    
    no_proc_available = cpu_count()
    if no_proc >= no_proc_available:
        msg.debuginfo('Exceeded the number of available processors')
        msg.debuginfo(str('User input: {}, Available: {}'.format(no_proc,no_proc_available)))
        msg.debuginfo(str('Number of Process was changed: {} >> {}'.format(no_proc, no_proc-2)))
        no_proc = no_proc_available - 2
    
    DB_config_split =  np.array_split(DB_config,no_proc)
    
    i=0
    # Get size values about splited configDB
    size_configDB_split=[]
    for i in range(no_proc):
        size_configDB_split.append(np.shape(DB_config_split[i])[0])    
        if size_configDB_split[i] != size_configDB_split[i-1]:
            last_max_DB = i
    
    msg.debuginfo(str('Size of the splited config DB: {}'.format(size_configDB_split)))
    
    max_iter = max(size_configDB_split)
            
    """
    max_iter = 1은 테스트를 위한 라인입니다.
    """         
    # max_iter = 1
    min_iter = min(size_configDB_split)
       
    msg.debuginfo('====================')
    line=0 # no_Airfoil at sepertated configuration DB
    
    while line < max_iter:
               
        if line > min_iter - 1:
            no_proc = last_max_DB
        
        progress=('Progress: '+str(line+1)+'/'+str(max_iter))
        stdout.write('\r'+progress)
        
        try:
            # Make CST Airfoil
            i=0
            
            pool = ThreadPool(no_proc)
            for i in range(no_proc):
                wl = DB_config_split[i][line, :4]
                wu = DB_config_split[i][line,4: ]
                                
                result = pool.apply_async(check_thickness, args = (wl, wu))
                thick = result.get(timeout = 1)
                if np.size(thick) > 0:
                    list_maxThickness.append(thick)
                    list_configDB_filtered.append(np.append(wl, wu))

            pool.close()
            pool.join()
            
         
            line += 1
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = exc_info()
            message1 = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
            Log.log(message1)
            message2 = str('Error Occured in progress: {}/{}'.format(line+1,max_iter))
            msg.debuginfo(message2)
            msg.debuginfo(progress)

            line = max_iter