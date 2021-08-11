# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 13:31:26 2017

@author: K_LAB
"""

"""
Info
====
Run the Xfoil Automatically
Using CST Curve
"""
 
from subprocess import Popen, PIPE
from time import time
from os import getcwd, chdir, remove
from os import path as ospath
from sys import path as syspath
from sys import exc_info

direct_work=getcwd()
# Find Code Directory
direct_code=ospath.dirname(ospath.realpath(__file__))
# If the code directory is not in PATH, add directory to import function
if direct_code not in syspath:
    syspath.append(direct_code)
direct_DB=ospath.join(direct_code,"DB")
    
import CST_Rinput as Rin

def runXfoil(no_proc, Re=3.0e6, M=0.2):
    
    var, val = Rin.Rinput(ospath.join(direct_code,'Input'),'Xfoil setting.txt',1)

##---------- XFOIL Setting ----------##
    Iter=val[0]
    AoA_min=float(val[1])
    AoA_max=float(val[2])
    AoA_step=val[3]
    timelim = int(val[4])
##-----------------------------------##
    
    direct_Temp=ospath.join(direct_DB,"Temp")
    direct_XFOIL=ospath.join(direct_Temp,"xfoil.exe")
    chdir(direct_Temp)
    CoordData='Temp config_'+str(no_proc)+'.txt'
    Savefile='Temp analyzed_'+str(no_proc)+'.txt'
    if ospath.isfile(ospath.join(direct_Temp,Savefile)):
        remove(ospath.join(direct_Temp,Savefile))
    
    command=str("plop\n g\n \n"+\
                "load " + CoordData+"\n" +\
                "oper\n" +\
                "iter\n" + str(Iter) + "\n" + \
                "visc\n" + str(Re) + "\n" + \
                "m\n" + str(M) + "\n" +\
                "pacc\n" +  Savefile + "\n \n" +\
                "aseq\n" + str(AoA_min) + "\n" +\
                str(AoA_max) + "\n" +\
                str(AoA_step) + "\n" +\
                "\n \n \n quit\n")
    try:
        p=Popen(direct_XFOIL,shell=False,stdin=PIPE,stdout=PIPE,stderr=None, encoding='utf-8')
        try:    
            p.communicate(command,timeout=timelim)
            p.kill()
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = exc_info()
            p.kill()
            
    except Exception as e:
        p.kill()
        exc_type, exc_obj, exc_tb = exc_info()

def runXfoil_custom(no_proc,Iter, AoA_min, AoA_max, AoA_step, Re=3.0e6, M=0.2):
    
    var, val = Rin.Rinput(ospath.join(direct_code,'Input'),'Xfoil setting.txt',1)

##---------- XFOIL Setting ----------##
    # Iter=val[0]
    timelim = int(val[4])
##-----------------------------------##
    
    direct_Temp=ospath.join(direct_DB,"Temp")
    direct_XFOIL=ospath.join(direct_Temp,"xfoil.exe")
    chdir(direct_Temp)
    CoordData='Temp config_'+str(no_proc)+'.txt'
    Savefile='Temp analyzed_'+str(no_proc)+'.txt'
    if ospath.isfile(ospath.join(direct_Temp,Savefile)):
        remove(ospath.join(direct_Temp,Savefile))
    
    command=str("plop\n g\n \n"+\
                "load " + CoordData+"\n" +\
                "oper\n" +\
                "iter\n" + str(Iter) + "\n" + \
                "visc\n" + str(Re) + "\n" + \
                "m\n" + str(M) + "\n" +\
                "pacc\n" +  Savefile + "\n \n" +\
                "aseq\n" + str(AoA_min) + "\n" +\
                str(AoA_max) + "\n" +\
                str(AoA_step) + "\n" +\
                "\n \n \n quit\n")
    try:
        p=Popen(direct_XFOIL,shell=False,stdin=PIPE,stdout=PIPE,stderr=None, encoding='utf-8')
        try:    
            p.communicate(command,timeout=timelim)
            p.kill()
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = exc_info()
            p.kill()
            
    except Exception as e:
        p.kill()
        exc_type, exc_obj, exc_tb = exc_info()

if __name__ == '__main__':
    time_start = time()
    runXfoil(0)
    time_run = time()-time_start
