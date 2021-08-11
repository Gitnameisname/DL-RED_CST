# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:04:03 2017

@author: K_LAB
"""

"""
Info
=====
Generate Data Base
Input value is Parameter and Aerodynamic Coefficient
Parameter has 3 value and Aerodynmic has 5 value
"""

from os import getcwd, remove
from os import path as ospath
from sys import path as syspath
from sys import exc_info

from numpy import shape

import CST_message as msg
import CST_Log as Log

direct_work = getcwd()
direct_code = ospath.dirname(ospath.realpath(__file__))

if direct_code not in syspath:
    syspath.append(direct_code)

direct_DB=ospath.join(direct_code,"DB")

# CACDB = Configuration & Condition               
def Config_DB(DBname,para_config):
    npsize=shape(para_config)
    print(npsize)
    i=0
    direct_file=ospath.join(direct_DB,DBname)
    if ospath.isfile(direct_file):
        remove(direct_file)
        msg.debuginfo(DBname+': File was removed')
        
    try:
        f=open(direct_file,'w')
        f.write('Configuration & Air Condition DB\n')
        f.write('      wl_1      wl_2      wl_3      wl_4      wu_1      wu_2      wu_3      wu_4\n')
        f.write(' ========= ========= ========= ========= ========= ========= ========= =========\n')    
        i=0
        while i < npsize[0]:
            f.write("{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}\n"\
                    .format(para_config[i,0],para_config[i,1],para_config[i,2],para_config[i,3],\
                            para_config[i,4],para_config[i,5],para_config[i,6],para_config[i,7]))
            i=i+1
        f.close()
        
    except Exception as e:
        f.close()
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)

def Config2CAC_DB(DBname,para_config,Re = [3e6], Mach = [0.2]):
    npsize=shape(para_config)
    i=0
    direct_file=ospath.join(direct_DB,DBname)
    if ospath.isfile(direct_file):
        remove(direct_file)
        msg.debuginfo(DBname+': File was removed')
        
    try:
        f=open(direct_file,'w')
        f.write('Configuration & Air Condition DB\n')
        f.write('      wl_1      wl_2      wl_3      wl_4      wu_1      wu_2      wu_3      wu_4        Re      Mach\n')
        f.write(' ========= ========= ========= ========= ========= ========= ========= ========= ========= =========\n')    
        k = 0
        for k in range(len(Re)):
            j = 0
            for j in range(len(Mach)):
                i=0
                while i < npsize[0]:
                    f.write("{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.0f}{:10.5f}\n"\
                            .format(para_config[i,0],para_config[i,1],para_config[i,2],para_config[i,3],\
                                    para_config[i,4],para_config[i,5],para_config[i,6],para_config[i,7],\
                                    Re[k], Mach[j]))
                    i=i+1
        f.close()
        
    except Exception as e:
        f.close()
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)

def CAC_DB(DBname,CAC):
    npsize=shape(CAC)
    i=0
    direct_file=ospath.join(direct_DB,DBname)
    if ospath.isfile(direct_file):
        remove(direct_file)
        msg.debuginfo(DBname+': File was removed')
        
    try:
        f=open(direct_file,'w')
        f.write('Configuration & Air Condition DB\n')
        f.write('        wl_1        wl_2        wl_3        wl_4        wu_1        wu_2        wu_3        wu_4          Re        Mach\n')
        f.write(' =========== =========== =========== =========== =========== =========== =========== =========== =========== ===========\n')    
        i=0
        while i < npsize[0]:
            f.write(" {:11.5f} {:11.5f} {:11.5f} {:11.5f} {:11.5f} {:11.5f} {:11.5f} {:11.5f} {:11.0f} {:11.5f}\n"\
                    .format(CAC[i,0],CAC[i,1],CAC[i,2],CAC[i,3],\
                            CAC[i,4],CAC[i,5],CAC[i,6],CAC[i,7],\
                            CAC[i,8],CAC[i,9]))
            i=i+1
        f.close()
        
    except Exception as e:
        f.close()
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)
        
def CSTDB_gen(DBname):
    direct_file=ospath.join(direct_DB,DBname)
    if ospath.isfile(direct_file):
        remove(direct_file)
    msg.debuginfo('Create DB as "{}"'.format(DBname))
    try:
        f=open(direct_file,'w')    
        f.write('CST digit {}\n'.format(DBname))
        f.write('        wl_1        wl_2        wl_3        wl_4'+\
                '        wu_1        wu_2        wu_3        wu_4'+\
                '          Re        Mach'+\
                '         Cl0        Cla0      Cl_max  AoA_Cl_max'+\
                '         Cm0        Cma0'+\
                '      Cd_min    ClCd_max\n')
        f.write(' =========== =========== =========== ==========='+\
                ' =========== =========== =========== ==========='+\
                ' =========== ==========='+\
                ' =========== =========== =========== ==========='+\
                ' =========== ==========='+\
                ' =========== ===========\n')
        f.close()
    except Exception as e:
        f.close()
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)
        return -1

def CSTDB(DBname,dataset):
    direct_file=ospath.join(direct_DB,DBname)
    
    if not ospath.isfile(direct_file):
        message = str('File not exist: "{}"'.format(DBname))
        msg.debuginfo(message)
        CSTDB_gen(DBname)
        message = str('Make the file: "{}"'.format(DBname))
        msg.debuginfo(message)
        
    npsize=shape(dataset)
    if len(npsize) == 1:
        try:
#            message = str('Write the data: '+ DBname)
#            msg.debuginfo(message)
            f=open(direct_file,'a')
            f.write(" {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                    " {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                    " {:11.0f} {:11.3f}"\
                    " {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                    " {:11.5f} {:11.5f}"\
                    " {:11.5f} {:11.5f}\n"\
                    .format(dataset[0],dataset[1],dataset[2],dataset[3],\
                            dataset[4],dataset[5],dataset[6],dataset[7],\
                            dataset[8],dataset[9],\
                            dataset[10],dataset[11],dataset[12],dataset[13],\
                            dataset[14],dataset[15],\
                            dataset[16],dataset[17]))
            f.close()
            
        except Exception as e:
            f.close()
            exc_type, exc_obj, exc_tb = exc_info()
            message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
            Log.log(message)
            return -1
        
    elif len(npsize) == 2:
        try:
#            message = str('Write the data: '+ DBname)
#            msg.debuginfo(message)
            f=open(direct_file,'a')
            i=0
            for i in range(npsize[0]):
                f.write(" {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                        " {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                        " {:11.0f} {:11.3f}"\
                        " {:11.5f} {:11.5f} {:11.5f} {:11.5f}"\
                        " {:11.5f} {:11.5f}"\
                        " {:11.5f} {:11.5f}\n"\
                        .format(dataset[i][0],dataset[i][1],dataset[i][2],dataset[i][3],\
                                dataset[i][4],dataset[i][5],dataset[i][6],dataset[i][7],\
                                dataset[i][8],dataset[i][9],\
                                dataset[i][10],dataset[i][11],dataset[i][12],dataset[i][13],\
                                dataset[i][14],dataset[i][15],\
                                dataset[i][16],dataset[i][17]))
            f.close()
            
        except Exception as e:
            f.close()
            exc_type, exc_obj, exc_tb = exc_info()
            message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
            Log.log(message)
            return -1
        
    else:
        message = str('Size of dataset is wrong: {}'.format(npsize))
        msg.debuginfo(message)
        
def CST_stats(list_folder, DBname, dataset):
    direct_file=ospath.join(ospath.join(direct_code,'Analyzed DB'),'Stats',DBname)
    if ospath.isfile(direct_file):
        remove(direct_file)
    
    iter_max = shape(dataset)[0]    
    
    # Initialize the DB file format
    if not ospath.isfile(direct_file):
        message = 'Create DB as "{}"'.format(DBname)
        msg.debuginfo(message)
        try:
            f=open(direct_file,'w')    
            f.write('CST Statistics {}\n'.format(DBname))
            f.write('       Cases'+\
                    '        wl_1        wl_2        wl_3        wl_4'+\
                    '        wu_1        wu_2        wu_3        wu_4'+\
                    '          Re        Mach'+\
                    '         Cl0        Cla0      Cl_max  AoA_Cl_max'+\
                    '         Cm0        Cma0'+\
                    '      Cd_min    ClCd_max\n')
            f.write(' ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== ==========='+\
                    ' =========== ===========\n')
            f.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = exc_info()
            message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
            Log.log(message)
            f.close()
            return -1

    try:
        i=0
        f=open(direct_file,'a')
        for i in range(iter_max):
            f.write('{:>12s}'\
                    '{:12.5f}{:12.5f}{:12.5f}{:12.5f}'\
                    '{:12.5f}{:12.5f}{:12.5f}{:12.5f}'\
                    '{:12.0f}{:12.3f}'\
                    '{:12.5f}{:12.5f}{:12.5f}{:12.5f}'\
                    '{:12.5f}{:12.5f}'\
                    '{:12.5f}{:12.5f}\n'\
                    .format(list_folder[i][:11],\
                            dataset[i][0],dataset[i][1],dataset[i][2],dataset[i][3],\
                            dataset[i][4],dataset[i][5],dataset[i][6],dataset[i][7],\
                            dataset[i][8],dataset[i][9],\
                            dataset[i][10],dataset[i][11],dataset[i][12],dataset[i][13],\
                            dataset[i][14],dataset[i][15],\
                            dataset[i][16],dataset[i][17]))
        f.close()
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)
        f.close()
        return -1