# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 15:26:19 2018

@author: K-AI_LAB
"""

"""
Info
=====
Search the performance characteristics from analyzed data
"""

from os import getcwd
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
direct_tempDB = ospath.join(direct_DB,"Temp")

import CST_CalADC as CalADC
import CST_message as msg
import CST_Log as Log

def get_AFconfig(direct_file):

    x=[]
    y=[]
    f=open(direct_file,'r')
    i=0
    # Coefficient is recorded from the 13th line
    start_line=2
    
    while True:
        line = f.readline()
        i=i+1
        # Read Coefficients
        if i > start_line - 1:
            coord=str(line) # Coefficient
            temp=coord.split(' ')
            j=0
            k=0
            while j < len(temp):
                if temp[j]=='':
                    j=j+1
                else:
                    if j == len(temp)-1:
                        temp[j]=temp[j].split('\n')[0]
                        y.append(float(temp[j]))
                    else:
                        x.append(float(temp[j]))
                        k=k+1
                    j=j+1
        if not line:
            break    
    f.close()
    
    config=[]
    config.append(x)
    config.append(y)
    
    return config

def get_AFaero(direct_file):
    f=open(direct_file,'r')
    i=0
    # Coefficient is recorded from the 13th line
    start_line=13
    while True:
        line = f.readline()
        i=i+1
        # 11th line is label
        if i == 11:
            C_List=str(line)
            temp=C_List.split(' ')
            label=[]
            j=0
            # Cut the label
            while j < len(temp):
                if temp[j]=='':
                    j=j+1
                else:
                    # last label has \n, so cut that value
                    if j == len(temp)-1:
                        temp[j]=temp[j].split('\n')[0]
                        label.append(temp[j])
                        vars()[temp[j]]=[]
                    else:
                        label.append(temp[j])
                        vars()[temp[j]]=[]
                    j=j+1
        # Read Coefficients
        if i > start_line - 1:
            C=str(line) # Coefficient
            temp=C.split(' ')
            j=0
            k=0
            while j < len(temp):
                if temp[j]=='':
                    j=j+1
                else:
                    if j == len(temp)-1:
                        k=len(label)-1
                        temp[j]=temp[j].split('\n')[0]
                        vars()[label[k]].append(float(temp[j]))
                    else:
                        vars()[label[k]].append(float(temp[j]))
                        k=k+1
                    j=j+1
        if not line:
            break    
    f.close()
    
    chara=[]
    chara.append(vars()[label[0]])
    chara.append(vars()[label[1]])
    chara.append(vars()[label[2]])
    chara.append(vars()[label[4]])
    
    return chara


def Aerodataset(no_proc, loop, wl, wu, Re, Mach, AoA_cut):
   
    try:
        name_Temp_AFaero = 'Temp analyzed_'+str(no_proc)+'.txt'
        direct_AFfile=ospath.join(direct_tempDB,name_Temp_AFaero)
        
        chara=CalADC.run(direct_AFfile,AoA_cut)
        dataset = []
        if len(chara)>0:
            dataset.extend(wl)
            dataset.extend(wu)
            dataset.append(float(Re))
            dataset.append(float(Mach))
            dataset.extend(chara)
        
        else:
            dataset = []
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        message = msg.errorinfo(exc_type, exc_obj, exc_tb, e)
        Log.log(message)
        
    return dataset

def Update_Clmax(no_proc, loop, AF_chara, index, AoA_cut):

    name_Temp_AFaero = 'Temp analyzed_'+str(no_proc)+'.txt'
    direct_AFfile=ospath.join(direct_tempDB,name_Temp_AFaero)
    
    Updated_AFchara = AF_chara
    Updated_values = CalADC.Get_Clmax(direct_AFfile) 
    
    if len(Updated_values) > 0: 
        i = 0
        max_iter = len(index)
    
        while i < max_iter:
            Updated_AFchara[index[i]] = Updated_values[i]
            
            i += 1
            
        return Updated_AFchara
    
    else:
        
        return []
    
