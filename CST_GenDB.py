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
import subprocess as sp
import numpy as np
import time
import os
import sys

direct_work = os.getcwd()
direct_code = os.path.dirname(os.path.realpath(__file__))

if direct_code not in sys.path:
    sys.path.append(direct_code)

direct_DB=os.path.join(direct_code,"DB")

               
def ConfigDB(DBname,para_config):
    npsize=np.shape(para_config)
    i=0
    direct_file=os.path.join(direct_DB,DBname)
    if os.path.isfile(direct_file):
        os.remove(direct_file)
        
    f=open(direct_file,'w')
    f.write('Initial configuration DB\n')
    f.write('      wl_1      wl_2      wl_3      wl_4      wu_1      wu_2      wu_3      wu_4\n')
    f.write(' ========= ========= ========= ========= ========= ========= ========= =========\n')    
    while i < npsize[0]:
        f.write("{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}{:10.5f}\n"\
                .format(para_config[i,0],para_config[i,1],para_config[i,2],para_config[i,3],\
                        para_config[i,4],para_config[i,5],para_config[i,6],para_config[i,7]))
        i=i+1
    f.close()
        
def CSTDB(DBname,dataset):
    direct_file=os.path.join(direct_DB,DBname)
    if not os.path.isfile(direct_file):
        print('Create DB as "{}"'.format(DBname))
        try:
            f=open(direct_file,'w')    
            f.write('NACA 4 digit {}\n'.format(DBname))
            f.write('          N1          N2'+\
                    '        wl_1        wl_2        wl_3        wl_4'+\
                    '        wu_1        wu_2        wu_3        wu_4'+\
                    '         Cl0        Cla0      Cl_max  AoA_Cl_max'+\
                    '         Cm0        Cma0'+\
                    '      Cd_min    ClCd_max\n')
            f.write(' =========== ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== =========== =========== ==========='+\
                    ' =========== ==========='+\
                    ' =========== ===========\n')
            f.write("{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}\n"\
                    .format(dataset[0],dataset[1],\
                            dataset[2],dataset[3],dataset[4],\
                            dataset[7],dataset[6],dataset[5],\
                            dataset[8],dataset[9],dataset[10],dataset[11],\
                            dataset[12],dataset[13],\
                            dataset[14],dataset[15],dataset[16],dataset[17]))
            f.close()
        except:
            f.close()
            print("while making {}, Error occur".format(DBname) )
            return -1

    else:
        try:
            f=open(direct_file,'a')
            f.write("{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}"\
                    "{:12.5f}{:12.5f}\n"\
                    .format(dataset[0],dataset[1],\
                            dataset[2],dataset[3],dataset[4],\
                            dataset[7],dataset[6],dataset[5],\
                            dataset[8],dataset[9],dataset[10],dataset[11],\
                            dataset[12],dataset[13],\
                            dataset[14],dataset[15],dataset[16],dataset[17]))
            f.close()
            
        except:
            f.close()
            print("while Writing {}, Error occur".format(DBname))
            return -1