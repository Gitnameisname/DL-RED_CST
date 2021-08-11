# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 23:39:02 2018

@author: K-AI_LAB
"""

"""
Info
=====
DLED_CST log file
"""
from os import getcwd, remove
from os import path as ospath
from sys import path as syspath
from sys import exc_info

import datetime

import CST_message as msg
   
direct_work=getcwd()
# Find Code Directory
direct_code=ospath.dirname(ospath.realpath(__file__))
# If the code directory is not in PATH, add directory to import function
if direct_code not in syspath:
    syspath.append(direct_code)
direct_log=ospath.join(direct_code,"log")
direct_logfile = ospath.join(direct_log,'log.txt')

if ospath.isfile(direct_logfile):
    remove(direct_logfile)

def log(get_log):
    if not ospath.isfile(direct_logfile):
        f = open(direct_logfile,'w')
        dt = datetime.datetime.now()
        
        try:
            f.write('Created on {}-{}-{} {}:{}:{}\n'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
            f.write('Deep Learning Engineering Design: CST Airfoil\n')
            f.write('Cheol-Kyun Choi\n')
            f.write('====================================================================================================\n')
            f.write('# input.txt\n#\n')
                    
            inputfile = open(ospath.join(direct_code,'Input','input.txt'))
            lines = inputfile.readlines()
            
            for i in range(len(lines)):
                f.write(lines[i])
            
            f.write('\n#input.txt end\n')
            f.write('====================================================================================================\n')
            f.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = exc_info()
            msg_get = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
            f.write('{}\n'.format(exc_type))
            f.write(msg_get)
            f.close()
    
    if get_log != None:
        f = open(direct_logfile,'a')
        f.write(get_log)
        f.write('\n')
        f.close()
        
    elif get_log == None:
        f = open(direct_logfile,'a')
        f.write('\n')
        f.close()

def log_clear():
    if ospath.isfile(direct_logfile):
        remove(direct_logfile)