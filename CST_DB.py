# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 16:17:51 2018

@author: K-AI_LAB
"""

"""
Info
=====
Make Initial DB for CST airfoil
"""

from numpy import copy, array, array_split, shape, zeros, where, delete, expand_dims, size
from numpy import append as npappend
from numpy import round as npround

from os import getcwd, remove
from os import path as ospath
from sys import path as syspath
from sys import exc_info, stdout

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import time

direct_work=getcwd()
direct_code=ospath.dirname(ospath.realpath(__file__))
syspath.append(direct_code)

import CST_message as msg
import CST_Log as Log
import CST_writeDB as wDB
import CST_Rinput as Rin
import CST_AF
import CST_ReadDB as ReadDB
import CST_RunXfoil
import CST_Dataset as AFdataset
import CST_exactClmax as exactClmax

name_inputfolder = 'Input'
name_inputfile = 'input.txt'
Log.log_clear()
Log.log(None)

# Initialize config. parameters #
# Fixed parameters #
dz = 0.  # Fix in this version
N = 200  # The number of point 

## Make Initial DB ##
direct_DB = ospath.join(direct_code,'DB')

def Init_AFDB(): # Configurer & Air Condition DB = CAC#
    time_start = time.time()
    
    # Configuration DB 생성 #
    filename_Config = 'Config DB 1.txt'
    if not ospath.isfile(ospath.join(direct_DB,filename_Config)):
        message = 'DB cannot be found: ' + filename_Config
        msg.debuginfo(message)
        Config_DB(filename_Config, 0, 0)
    
    else:
        message = 'Existence Check: ' + filename_Config
        msg.debuginfo(message)
        
    # Filtering Configuration DB #
    # 최대 두께가 3% 이상, 20% 이하인 에어포일만 골라낸다.
    filename_config_filtered = 'Config DB filtered 1.txt'
    
    if not ospath.isfile(ospath.join(direct_DB,filename_config_filtered)):
        message = 'DB cannot be found: ' + filename_config_filtered
        msg.debuginfo(message)
        Filtering_ConfigDB(filename_Config, filename_config_filtered)
        
    else:
        message = 'Existence Check: ' + filename_config_filtered
        msg.debuginfo(message)

    # CAC DB - Configuration and Air Condition DB - 를 만듭니다.
    filename_CACDB = 'CAC DB init 1.txt'
    if not ospath.isfile(ospath.join(direct_DB, filename_CACDB)):
        message = 'DB cannot be found: ' + filename_CACDB
        msg.debuginfo(message)
        Config2CACDB(filename_config_filtered, filename_CACDB)
        
    else:
        message = 'Checked Existence: ' + filename_CACDB
        msg.debuginfo(message)
    
    # CAC DB 초기값으로 해석을 돌린다. #
    filename_AFDB_init = 'CST Airfoil DB_init 1.txt'
    if not ospath.isfile(ospath.join(direct_DB,filename_AFDB_init)):
        message = 'DB cannot be found: ' + filename_AFDB_init
        msg.debuginfo(message)
        
        CAC2AFDB(1, filename_CACDB, filename_AFDB_init)
    else:
        message = 'Checked Existence: CST Airfoil DB_init 1 DB'
        msg.debuginfo(message)
    
    # 초기 에어포일 DB에서 유효한 것들만 골라낸다. #
    filename_AFDB_filtered = 'CST Airfoil DB_init filtered 1.txt'
    if not ospath.isfile(ospath.join(direct_DB, filename_AFDB_filtered)):
        message = 'DB cannot be found: ' + filename_AFDB_filtered
        msg.debuginfo(message)
        filename_AFDB = 'CST Airfoil DB_init 1.txt'
        result_Postprocessing = AFDB_Postprocessing(filename_AFDB, filename_AFDB_filtered)
    else:
        message = 'Checked Existence: ' + filename_AFDB_filtered
        msg.debuginfo(message)
        result_Postprocessing = 0
    
    # 이 값들을 이용해서 확장된 CAC DB를 만든다. #
    filename_CACDB_exp = 'CAC init Expand DB 1.txt'
    if result_Postprocessing == 1:
        filename_AFDB = filename_AFDB_filtered
        if not ospath.isfile(ospath.join(direct_DB, filename_CACDB_exp)):
            message = 'DB cannot be found: ' + filename_CACDB_exp
            msg.debuginfo(message)
            CACDB_expand(filename_AFDB, filename_CACDB_exp)
        else:
            message = 'Checked Existence: ' + filename_CACDB_exp
            msg.debuginfo(message)
    else:
        filename_AFDB = filename_AFDB
    
    
        
    # CAC expand에는 이미 앞서 성능을 해석한 에어포일들도 있다. #
    # 이들만 줄여도 6시간은 확보할 수 있다. #
    # 해석해야 할 에어포일은 약 12만개로서, 12,000개였던 initial DB의 약 10배 #
    # 약 60시간이 걸리므로, 2일하고 반나절이 걸린다. #
    if not ospath.isfile(ospath.join(direct_DB,'CST Airfoil DB Expand 1.txt')):
        message = 'Cannot found the CST Airfoil DB Expand 1 DB'
        msg.debuginfo(message)
        filename_CACDB = 'CAC init Expand DB 1.txt'
        filename_AFDB = 'CST Airfoil DB Expand 1.txt'
        CAC2AFDB(1, filename_CACDB, filename_AFDB)
    else:
        message = 'Checked Existence: CST Airfoil DB Expand 1 DB'
        msg.debuginfo(message)


    # 에어포일 DB에서 유효한 것들만 골라낸다. #
    if not ospath.isfile(ospath.join(direct_DB,'CST Airfoil DB sorted 1.txt')):
        message = 'Cannot found the CST Airfoil DB sorted 1 DB'
        msg.debuginfo(message)
        filename_AFDB = 'CST Airfoil DB Expand 1.txt'
        filename_AFDB_revised = 'CST Airfoil DB sorted 1.txt'
        result_Postprocessing = AFDB_Postprocessing(filename_AFDB, filename_AFDB_revised)
    else:
        message = 'Checked Existence: CST Airfoil DB sorted 1 DB'
        msg.debuginfo(message)
    
    # Clmax 값의 정밀도를 높인다. #
    if not ospath.isfile(ospath.join(direct_DB,'CST Airfoil DB 1.txt')):
        message = 'Cannot found the CST Airfoil DB 1 DB'
        msg.debuginfo(message)
        DBname_AFDB = 'CST Airfoil DB sorted 1.txt'
        DBname_AFDB_Enhanced = 'CST Airfoil DB 1.txt'
        exactClmax.UpdateDB_Clmax(1, DBname_AFDB, DBname_AFDB_Enhanced)
    else:
        message = 'Checked Existence: CST Airfoil DB 1 DB'
        msg.debuginfo(message)
    
    time_run = time.time()-time_start    
    msg.debuginfo('All Initial DB are ready')
    msg.debuginfo('Initial configuration and air condition DB was built')
    msg.debuginfo('Run time: {:.2f} sec, {:.2f} min\n'.format(time_run,time_run/60))

def Config_DB(filename_Config, boundary_low = 0., boundary_up = 0.):
    time_start = time.time()
    if boundary_low == 0. and boundary_up == 0.:
            message = 'Makes ' + filename_Config
            msg.debuginfo(message)
            
    else:
        message = 'Makes ' + filename_Config + ' with expanded boundary'
        msg.debuginfo(message)
        message = 'with expand low boundary: ' + str(boundary_low)
        msg.debuginfo(message)
        message = 'with expand upper boundary: ' + str(boundary_up)
        msg.debuginfo(message)
    
    # min max of variables #
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,3)    
    return_val = Rin.Conv_vals(var, val)

    wu_max =  return_val[0]
    wu_min =  return_val[1]
    wl_max =  return_val[2]
    wl_min =  return_val[3]

    i = 0
    for i in range(len(return_val[0])):

        wu_max[i] =  return_val[0][i] + boundary_up
        wu_min[i] =  return_val[1][i] + boundary_low
        wl_max[i] =  return_val[2][i] + boundary_up
        wl_min[i] =  return_val[3][i] + boundary_low

    wu_step = return_val[4]
    wl_step = return_val[5]
    
    # Variables #
    wu = copy(wu_min)
    wl = copy(wl_min)

    on_off = 1
    config_para=zeros([0,8])
    
    while on_off == 1:
        config_para = npappend(config_para, array([[wl[0], wl[1], wl[2], wl[3], wu[0], wu[1], wu[2], wu[3]]]), axis=0)

        # To clean the round off error, using round command
        # First combination of repetition
        wu[3] = npround((wu[3] + wu_step[3])*10)/10
        
        if wu[3] > wu_max[3]:
            wl[3] = npround((wl[3] + wl_step[3])*10)/10 
            wu[3] = max(wu_min[3],wl[3])
        
        if wl[3] > wl_max[3]:
            wu[3] = wu_min[3]
            wl[3] = wl_min[3]
            
            wu[2] = npround((wu[2] + wu_step[2])*10)/10
        
        if wu[2] > wu_max[2]:
            wl[2] = npround((wl[2] + wl_step[2])*10)/10 
            wu[2] = max(wu_min[2],wl[2])
        
        if wl[2] > wl_max[2]:
            wu[2] = wu_min[2]
            wl[2] = wl_min[2]
            
            wu[1] = npround((wu[1] + wu_step[1])*10)/10
            
        # Second combination of repetition
        if wu[1] > wu_max[1]:
            wl[1] = npround((wl[1] + wl_step[1])*10)/10 
            wu[1] = max(wu_min[1],wl[1])
            
        if wl[1] > wl_max[1]:
            wu[1] = wu_min[1]
            wl[1] = wl_min[1]
            
            wu[0] = npround((wu[0] + wu_step[0])*10)/10
    
        # Third combination of repetition
        if wu[0] > wu_max[0]:
            wl[0] = npround((wl[0] + wl_step[0])*10)/10 
            wu[0] = max(wu_min[0],wl[0])
            
        if wl[0] > wl_max[0]:
            on_off = 0

    wDB.Config_DB(filename_Config, config_para)
    
    time_run = time.time()-time_start
    msg.debuginfo('Configuration Data was built')
    msg.debuginfo('DB build time: {:.2f} sec, {:.2f} min\n'.format(time_run,time_run/60))

# 어떤 에어포일의 형상 파라미터 wl과 wu를 받으면, 해당 에어포일의 최대 두께를 측정하고 반환합니다.
# plot_name 값을 입력받으면, 해당 에어포일의 그래프를 png 파일로 저장합니다.
def check_thickness(wl, wu):
    dz = 0.
    N = 200
    airfoil = CST_AF.CST_shape(0.5, 1.0, wl, wu, dz, N)
    coord = airfoil.airfoil_coor()

    thick = []

    i = 0
    for i in range(99):
        thick.append(coord[1][i+1]-coord[1][199-i])
        
    thick_max = max(thick)
   
    if thick_max >= 0.03 and thick_max <= 0.2:

        return thick_max
    
    else:
        return []

def Filtering_ConfigDB(filename_config, filename_config_filtered):
    
    DB_config = ReadDB.Read(filename_config)
    DB_config_filtered = zeros([0,8])
    list_maxThickness = []
    
    # 가용할 수 있는 스레드의 수를 구합니다.
    # 사용자의 입력값을 기본으로 하되, 만약 사용자값이 가용 값을 넘어서면,
    # 최대 사용할 수 있는 스레드 수의 -2 개를 사용합니다.
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,4)
    no_proc = int(val[0])
    
    no_proc_available = cpu_count()
    if no_proc >= no_proc_available:
        msg.debuginfo('Exceeded the number of available processors')
        msg.debuginfo(str('User input: {}, Available: {}'.format(no_proc,no_proc_available)))
        msg.debuginfo(str('Number of Process was changed: {} >> {}'.format(no_proc, no_proc-2)))
        no_proc = no_proc_available - 2
    
    # Configuration DB를 no_proc 수로 나눕니다.
    DB_config_split =  array_split(DB_config,no_proc)

    i=0
    # 나눠진 Configuration DB들의 크기를 구하고,
    # Configuration DB의 크기가 변하는 위치를 찾습니다.
    # 해당 값을 통해 마지막 연산 시, 사용하는 스레드의 수를 줄입니다.
    size_configDB_split=[]
    for i in range(no_proc):
        size_configDB_split.append(shape(DB_config_split[i])[0])    
        if size_configDB_split[i] != size_configDB_split[i-1]:
            last_max_DB = i
            
    msg.debuginfo(str('Size of the splited config DB: {}'.format(size_configDB_split)))
    
    max_iter = max(size_configDB_split)
    
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
                thick = result.get(None)
                if size(thick) > 0:
                    list_maxThickness.append(thick)
                    DB_config_filtered = npappend(DB_config_filtered, expand_dims(npappend(wl,wu), axis = 0), axis = 0)

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
    
    wDB.Config_DB(filename_config_filtered, DB_config_filtered)
    
    return list_maxThickness
    
def Config2CACDB(filename_config_filtered, filename_CAC):
    DB_config = ReadDB.Read(filename_config_filtered)
    wDB.Config2CAC_DB(filename_CAC,DB_config[:,:8],Re=[2e6],Mach=[0.2])

def CACDB_expand(filename_AFDB_init, filename_CAC_exp):
    
    DB_config = ReadDB.Read(filename_AFDB_init)
    wDB.Config2CAC_DB(filename_CAC_exp, DB_config[:,:8], Re = [2e6, 4e6, 6e6, 8e6, 10e6], Mach = [0.1,0.2,0.3,0.4,0.5])

def Predict_Config2CACDB(filename_Predict, filename_Answer, filename_CACDB):
    # filename_Predict = 'CST Prediction DB ' + str(loop) + '.txt'
    # filename_Answer = 'CST Answer DB_raw ' + str(loop) + '.txt'
    # filename_CACDB = 'CST Prediction CAC DB ' + str(loop) + '.txt'
    
    if ospath.isfile(ospath.join(direct_DB,filename_CACDB)):
        remove(ospath.join(direct_DB,filename_CACDB))
    
    DB_Predict = ReadDB.Read(filename_Predict)
    DB_Answer = ReadDB.Read(filename_Answer)
    
    Aircond = DB_Answer[:,8:10]
    DB_CAC = npappend(DB_Predict,Aircond,axis=1)
    wDB.CAC_DB(filename_CACDB,DB_CAC)
    msg.debuginfo(filename_CACDB +' was built')
    
def CAC2AFDB(loop, filename_CACDB, filename_AFDB):
    # Read initial DB and divide for multiprocessing ##
    # Read initial DB and divide for multiprocessing ##
    
    msg.debuginfo(None)
    msg.debuginfo('Start to Analyze Airfoils with XFOIL')
    
    # Make DB file #
    wDB.CSTDB_gen(filename_AFDB)
    
    time_start=time.time()
    
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,2)
    no_input = int(val[2])
    no_output = int(val[3])
    
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,4)
    no_proc = int(val[0])
    no_proc_fix = int(val[0])
    AoA_cut = int(val[1])
    
    # Check the input value: no_proc is over the available no_proc
    no_proc_available = cpu_count()
    if no_proc >= no_proc_available:
        msg.debuginfo('Exceeded the number of available processors')
        msg.debuginfo(str('User input: {}, Available: {}'.format(no_proc,no_proc_available)))
        msg.debuginfo(str('Number of Process was changed: {} >> {}'.format(no_proc, no_proc-2)))
        no_proc = no_proc_available - 2
        
    # If no_proc is under the availiable no_proc, do below
    
    try:
        CAC_DB = ReadDB.Read(filename_CACDB)
        split_CACDB = array_split(CAC_DB,no_proc)
        
        i=0
        # Get size values about splited configDB
        size_split_CACDB=[]
        for i in range(no_proc):
            size_split_CACDB.append(shape(split_CACDB[i])[0])
            name_split_AFDB = 'split_AFDB'+str(i)
            vars()[name_split_AFDB] = zeros([0,no_input+no_output])
            
            if size_split_CACDB[i] != size_split_CACDB[i-1]:
                last_max_DB = i
            
        msg.debuginfo(str('Size of the splited config DB: {}'.format(size_split_CACDB)))
        
        # Seperated DB can have differente size #
        # for prevent the error, record max/min size of split DB#
        max_iter = max(size_split_CACDB)
        
        """
        max_iter = 1은 테스트를 위한 라인입니다.
        """         
        # max_iter = 1
        min_iter = min(size_split_CACDB)
        
        msg.debuginfo(None)
        msg.debuginfo(str('XFOIL Analysis Start'))
        
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
                for i in range(no_proc):
                    N1=0.5
                    N2=1.0
                    wl=[split_CACDB[i][line,0],split_CACDB[i][line,1],split_CACDB[i][line,2],split_CACDB[i][line,3]]
                    wu=[split_CACDB[i][line,4],split_CACDB[i][line,5],split_CACDB[i][line,6],split_CACDB[i][line,7]]
                    
                    AF = CST_AF.CST_shape(N1, N2, wl, wu, dz, N)
                    AF.airfoil_coor()
                    
                # Xfoil analysis with multiprocessing
                pool = ThreadPool(no_proc)
                ## If multiprocessing does not work well, check that below
                # 2nd input should be a tuple type
                # check the function to use
                i=0
                for i in range(no_proc):
                    pool.apply_async(CST_RunXfoil.runXfoil,args=(i,split_CACDB[i][line,8],split_CACDB[i][line,9]))
                pool.close()
                pool.join()
                
                i=0
                for i in range(no_proc):
                    name_split_AFDB = 'split_AFDB' + str(i)
                    wl=[split_CACDB[i][line,0],split_CACDB[i][line,1],split_CACDB[i][line,2],split_CACDB[i][line,3]]
                    wu=[split_CACDB[i][line,4],split_CACDB[i][line,5],split_CACDB[i][line,6],split_CACDB[i][line,7]]
                    airfoildata = AFdataset.Aerodataset(i, loop, wl, wu,split_CACDB[i][line,8],split_CACDB[i][line,9], AoA_cut)
                    
                    if len(airfoildata) > 0:
                        vars()[name_split_AFDB] = npappend(vars()[name_split_AFDB],array([airfoildata]),0)
         
                line += 1
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = exc_info()
                message1 = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
                Log.log(message1)
                message2 = str('Error Occured in progress: {}/{}'.format(line+1,max_iter))
                msg.debuginfo(message2)
                msg.debuginfo(progress)
                line = max_iter
        
        # Gather all splited airfoil DB to one DB
        Full_airfoilDB = zeros([0,no_input+no_output])
        for i in range(no_proc_fix):
            name_split_AFDB = 'split_AFDB'+str(i)
            Full_airfoilDB = npappend(Full_airfoilDB, vars()[name_split_AFDB],0)
           
        print('\n')
        msg.debuginfo('====================')
        msg.debuginfo('XFOIL Analysis Ended')
        time_run = time.time()-time_start
        msg.debuginfo(str('Run Time: {:.2f} min, {:.2f} hr'.format(time_run/60,time_run/3600)))
        wDB.CSTDB(filename_AFDB,Full_airfoilDB)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)

def AFDB_Postprocessing(filename_AFDB, filename_AFDB_revised):
    
    msg.debuginfo('Airfoil DB revise')
    msg.debuginfo(str('DB type: ' + filename_AFDB))
        
    wDB.CSTDB_gen(filename_AFDB_revised)
    
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,4) # Xfoil Condition
    AoA_cut = float(val[1])
    
    AFDS = ReadDB.Read(filename_AFDB) # Airfoil dataset
    
    # Delete Airfoils that Max Cl AOA is over AoA cut
    if (max(AFDS[:,13]) > AoA_cut):
        AFDS_Descent = AFDS[AFDS[:,13].argsort()[::-1]]
        AoA_index = max(where(AFDS_Descent[:,13] >= AoA_cut)[0])
        AFDS_rev = AFDS_Descent[AoA_index:,:]
        
        i=0
        msg.debuginfo('Delete airfoils: Cdmin is zero or ClCd max is over than 999')
        while i < shape(AFDS_rev)[0]:
            if AFDS_rev[i,16] == 0 or AFDS_rev[i,-1] > 999:
                AFDS_rev = delete(AFDS_rev,i,0)
            else:
                i += 1
        
        msg.debuginfo(str('Delete airfoils: Cl max AoA over {} degree'.format(AoA_cut+1)))
        
        for i in range(shape(AFDS_rev)[0]):
            wDB.CSTDB(filename_AFDB_revised,AFDS_rev[i])
            
        message = str('File created: ' + filename_AFDB_revised)
        msg.debuginfo(message)
    
        return 1
        
    else:
        msg.debuginfo('Maximum value of CLmax AOA is: ' + str(max(AFDS[:,13])))
        msg.debuginfo("User's boundary value was: " + str(AoA_cut))
        
        return 0
        
def AFDB_Clmax_Enhance(loop, filename_AFDB, filename_AFDB_Enhanced):
    # Read initial DB and divide for multiprocessing ##
    # Read initial DB and divide for multiprocessing ##
    
    msg.debuginfo(None)
    msg.debuginfo('Start to Enhance Cl max with XFOIL')
    
    # Make DB file #
    wDB.CSTDB_gen(filename_AFDB_Enhanced)
    
    time_start=time.time()
    
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,2)
    no_input = int(val[2])
    no_output = int(val[3])
    
    var, val = Rin.Rinput(name_inputfolder,name_inputfile,4)
    no_proc = int(val[0])
    no_proc_fix = int(val[0])
    AoA_cut = int(val[1])
    
    # Check the input value: no_proc is over the available no_proc
    no_proc_available = cpu_count()
    if no_proc >= no_proc_available:
        msg.debuginfo('Exceeded the number of available processors')
        msg.debuginfo(str('User input: {}, Available: {}'.format(no_proc,no_proc_available)))
        msg.debuginfo(str('Number of Process was changed: {} >> {}'.format(no_proc, no_proc-2)))
        no_proc = no_proc_available - 2
        
    # If no_proc is smaller than the availiable no_proc, do below
    
    try:
        AFDB = ReadDB.Read(filename_AFDB)
        split_AFDB = array_split(AFDB,no_proc)
        
        i=0
        # Get size values about splited configDB
        size_split_AFDB=[]
        for i in range(no_proc):
            size_split_AFDB.append(shape(split_AFDB[i])[0])
            name_split_AFDB = 'split_AFDB'+str(i)
            vars()[name_split_AFDB] = zeros([0,no_input+no_output])
            
            if size_split_AFDB[i] != size_split_AFDB[i-1]:
                last_max_DB = i
            
        msg.debuginfo(str('Size of the splited config DB: {}'.format(size_split_AFDB)))
        
        # Seperated DB can have differente size #
        # for prevent the error, record max/min size of split DB#
        max_iter = max(size_split_AFDB)
        
        """
        max_iter = 1은 테스트를 위한 라인입니다.
        """         
        # max_iter = 1
        min_iter = min(size_split_AFDB)
        
        msg.debuginfo(None)
        msg.debuginfo(str('XFOIL Analysis Start'))
        
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
                for i in range(no_proc):
                    N1=0.5
                    N2=1.0
                    wl=[split_AFDB[i][line,0],split_AFDB[i][line,1],split_AFDB[i][line,2],split_AFDB[i][line,3]]
                    wu=[split_AFDB[i][line,4],split_AFDB[i][line,5],split_AFDB[i][line,6],split_AFDB[i][line,7]]
                    
                    AF = CST_AF.CST_shape(N1, N2, wl, wu, dz, N)
                    AF.airfoil_coor(i,line)
                    
                # Xfoil analysis with multiprocessing
                pool = ThreadPool(no_proc)
                ## If multiprocessing does not work well, check that below
                # 2nd input should be a tuple type
                # check the function to use
                i=0
                for i in range(no_proc):
                    pool.apply_async(CST_RunXfoil.runXfoil,args=(i,split_AFDB[i][line,8],split_AFDB[i][line,9]))
                pool.close()
                pool.join()
                
                i=0
                for i in range(no_proc):
                    name_split_AFDB = 'split_AFDB' + str(i)
                    wl=[split_AFDB[i][line,0],split_AFDB[i][line,1],split_AFDB[i][line,2],split_AFDB[i][line,3]]
                    wu=[split_AFDB[i][line,4],split_AFDB[i][line,5],split_AFDB[i][line,6],split_AFDB[i][line,7]]
                    airfoildata = AFdataset.Aerodataset(i, loop, wl, wu,split_AFDB[i][line,8],split_AFDB[i][line,9], AoA_cut)
                    
                    if len(airfoildata) > 0:
                        vars()[name_split_AFDB] = npappend(vars()[name_split_AFDB],array([airfoildata]),0)
         
                line += 1
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = exc_info()
                message1 = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
                Log.log(message1)
                message2 = str('Error Occured in progress: {}/{}'.format(line+1,max_iter))
                msg.debuginfo(message2)
                msg.debuginfo(progress)
                line = max_iter
        
        # Gather all splited airfoil DB to one DB
        Full_airfoilDB = zeros([0,no_input+no_output])
        for i in range(no_proc_fix):
            name_split_AFDB = 'split_AFDB'+str(i)
            Full_airfoilDB = npappend(Full_airfoilDB, vars()[name_split_AFDB],0)
           
        print('\n')
        msg.debuginfo('====================')
        msg.debuginfo('XFOIL Analysis Ended')
        time_run = time.time()-time_start
        msg.debuginfo(str('Run Time: {:.2f} min, {:.2f} hr'.format(time_run/60,time_run/3600)))
        wDB.CSTDB(filename_AFDB,Full_airfoilDB)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)

if __name__ == '__main__':
    Init_AFDB()
    