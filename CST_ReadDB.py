# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 12:48:40 2017

@author: K_LAB
"""

"""
Info
=====
Read DB file and return as Array
"""

from os import path as ospath
from numpy import zeros

import CST_message as msg

direct_code=ospath.dirname(ospath.realpath('__file__'))
    
def Read(name_file, DBdirect=ospath.join(direct_code,"DB")):
    print(DBdirect)
    ## Initialize function ##
    # filename is the name of reading file with extension
    direct_file=ospath.join(DBdirect,name_file)
    msg.debuginfo(str('Read the database: {}'.format(direct_file)))

    f=open(direct_file,'r')
    i=0
    while True:
        # Read line by line
        line = f.readline()
        # Second line is the label of Data
        if i == 1:
            C_List=str(line)
            temp=C_List.split(' ')
            label=[]
            j=0
            # Cut the label by label
            while j < len(temp):
                if temp[j]=='':
                    j=j+1
                # Cut \n of last label
                else:
                    if j == len(temp)-1:
                        temp[j]=temp[j].split('\n')[0]
                        label.append(temp[j])
                        # Create variables using the name of label
                        vars()[temp[j]]=[]
                    else:
                        # Create variables using the name of label
                        label.append(temp[j])
                        vars()[temp[j]]=[]
                    j=j+1
        
        # Skip the 3rd line >> this is the border line between label and values
        elif i > 2:
            C=str(line)
            temp=C.split(' ')
            j=0
            k=0
            while j < len(temp):
                # If none, go to next
                if temp[j]=='':
                    j=j+1
                else:
                    if j == len(temp)-1:
                        k=len(label)-1
                        temp[j]=temp[j].split('\n')[0]
                        # Create variables using the name of label
                        vars()[label[k]].append(temp[j])
                    else:
                        # Create variables using the name of label
                        vars()[label[k]].append(temp[j])
                        k=k+1
                    j=j+1
        # if the line end, break the roop
        if not line:
            break
        i=i+1
    f.close()
    
    # Initialize the return matrix
    mat=zeros([len(vars()[label[0]]),len(label)])
    i=0
    # Fill the matrix
    for i in range(len(label)):
        mat[:,i]=vars()[label[i]]
    return mat

def Read_datalist(filename, DBdirect=ospath.join(direct_code,"DB")):
    ## Initialize function ##
    # filename is the name of reading file with extension
    
    """def __init__(self, filename):"""
    # Check the workdirectory
    # and make [Filedirect]
    
    filedirect=ospath.join(DBdirect,filename)
    
    """def Read(self):"""
    f=open(filedirect,'r')
    i=0
    while i<2:
        # Read line by line
        line = f.readline()
        # Second line is the label of Data
        if i == 1:
            C_List=str(line)
            temp=C_List.split(' ')
            label=[]
            j=0
            # Cut the label by label
            while j < len(temp):
                if temp[j]=='':
                    j=j+1
                # Cut \n of last label
                else:
                    if j == len(temp)-1:
                        temp[j]=temp[j].split('\n')[0]
                        label.append(temp[j])
                        # Create variables using the name of label
                        vars()[temp[j]]=[]
                    else:
                        # Create variables using the name of label
                        label.append(temp[j])
                        vars()[temp[j]]=[]
                    j=j+1
        
        i=i+1
    f.close()
    
    return label

if __name__ == "__main__":
    CSTDB = Read('CST Airfoil DB 1.txt')
