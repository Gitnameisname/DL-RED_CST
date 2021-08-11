# -*- coding: utf-8 -*-
"""
Created on Fri May  4 13:56:01 2018

@author: K-AI_LAB
"""

"""
Info
=====
Read hyperparameter of the training model
"""

from os import path
from numpy import shape 

direct_code = path.dirname(path.realpath('__file__'))
    
def Rinput(name_folder,name_file,no):
    direct_file = path.join(direct_code,name_folder,name_file)
    f = open(direct_file)
    
    text = f.readlines()
    
    max_line = shape(text)[0]
    
    ## Get the information ##
    
    i = 0
    printswitch = 0
    variable = []
    value = []
    
    while i < max_line:
        line = text[i]
        
        if line[0] == str('$'):
            printswitch = 0
        if printswitch == 1:
            temp = line.split('\n')[0]
            temp = temp.split('\t')
            temp = list(filter(None,temp))
            if len(temp) == 2:
                variable.append(temp[0].split(':')[0])
                value.append(temp[-1])
        if line[0:2] == str('#'+str(no)):
            printswitch = 1
            
        i += 1
        
        
        
    return variable, value

def Conv_vals(variable, value):
    
    return_val=[]
    i=0
    for i in range(len(variable)):
        vars()[variable[i]] = value[i].split(',')        
        j=0
        for j in range(len(vars()[variable[i]])):
            vars()[variable[i]][j]=float(vars()[variable[i]][j])
        return_val.append(vars()[variable[i]])
        
    return return_val
    
               
if __name__ == "__main__":

    var, val = Rinput('Input','Input.txt',3)