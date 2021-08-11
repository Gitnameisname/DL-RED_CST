# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:54:45 2017

@author: K_LAB
"""

"""
Info
=====
Calculate Aerodynamic Characteristics
1.   2.     3.     4.         5.   6.     7.     8.
Cl0, Cla_0, Clmax, AoA_Clmax, Cm0, Cma_0, Cdmin, ClCdmax
"""

from numpy import shape, where, zeros
from numpy import append as npappend
from numpy import abs as npabs

def find_Clmax(Cl, AoA):
    
    Clmax = max(Cl)
    AoA_Clmax = AoA[where(Cl == Clmax)]   
        
    return Clmax, AoA_Clmax[0]

def run(filedirect,crit_AoA):
    
    ## Read File ##
    # =========== #
    # Read file and collect the aerodynamic data
    # Open file with 'r' - Read only
    f=open(filedirect,'r')
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
                        vars()[label[k]].append(temp[j])
                    else:
                        vars()[label[k]].append(temp[j])
                        k=k+1
                    j=j+1
        if not line:
            break    
    f.close()      
    
    ## Calculate Aerodynamic Characteristics ##
    # ======================================= #
    # Save the infomations at matrix
    # Initialize the matrix        
    mat=zeros([len(vars()[label[0]]),len(label)])
    # mat label
    # AoA, Cl, Cd, Cdp, Cm, Top Xtr, Bot Xtr
    #   0,  1,  2,   3,  4,       5,       6
    
    # Record labels
    for i in range(0,len(label),1):
        mat[:,i]=vars()[label[i]]
    
    # Only calculate ADC if over the number of criteria AoA cases are analyzed
    
    if shape(mat)[0] > crit_AoA:
        # There are two possible case
        # 1. File has the value at AoA 0 degree
        # 2. File does not have the value at AoA 0 degree
        # If AoA 0 is exist (Case1) 
        if 0 in mat[:,0]:
            # Find the index of AoA 0
            zero_P=where(mat[:,0] == 0)[0][0]
    
            # If there are AoA 0 + step, Calculate by zero, zero + step values
            if abs(mat[zero_P+1,0])<=abs(mat[zero_P-1,0]):
                Cl0  = mat[zero_P,1]
                Cla0 = (mat[zero_P+1,1]-mat[zero_P,1])/(mat[zero_P+1,0]-mat[zero_P,0])
                Cm0  = mat[zero_P,4]
                Cma0 = (mat[zero_P+1,4]-mat[zero_P,4])/(mat[zero_P+1,0]-mat[zero_P,0])
            # If AoA 0 + step does not exist, Calculate by zero - step, zero values
            elif abs(mat[zero_P+1,0])>abs(mat[zero_P-1,0]):
                Cl0  = mat[zero_P,1]
                Cla0 = (mat[zero_P,1]-mat[zero_P-1,1])/(mat[zero_P,0]-mat[zero_P-1,0])
                Cm0  = mat[zero_P,4]
                Cma0 = (mat[zero_P,4]-mat[zero_P-1,4])/(mat[zero_P,0]-mat[zero_P-1,0])

        # If AoA 0 does not exist (Case2)
        # Use the values near the AoA 0
        else:
            absAoA=npabs(mat[:,0])
            ref_P=[]
            # Find the index of nearest value from AoA 0
            ref_P.append(where(absAoA==min(absAoA))[0][0])
            # If the 0 deg AoA does not exist, Calculate by side values
            # If the min value is positive, use the before step value
            # that value is must the nearest negative value from AoA zero
            if mat[ref_P[0],0] > 0:
                ref_P.append(ref_P[0]-1)
                ref_P.sort()
            # If the min value is negative, use the next step value
            # that value is must the nearest positive value from AoA zero
            elif mat[ref_P[0],0] < 0:
                ref_P.append(ref_P[0]+1)
                ref_P.sort()
            # ref_P[0]: -A: position of highest negative AoA
            # ref_P[1]: +A: position of lowest positive AoA
            Cl0  = -1*mat[ref_P[0],0]*((mat[ref_P[1],1]-mat[ref_P[0],1]))/(mat[ref_P[1],0]-mat[ref_P[0],0])+mat[ref_P[0],1]
            Cla0 = (mat[ref_P[1],1]-mat[ref_P[0],1])/(mat[ref_P[1],0]-mat[ref_P[0],0])
            Cm0  = -1*mat[ref_P[0],0]*((mat[ref_P[1],4]-mat[ref_P[0],4]))/(mat[ref_P[1],0]-mat[ref_P[0],0])+mat[ref_P[0],4]
            Cma0 = (mat[ref_P[1],4]-mat[ref_P[0],4])/(mat[ref_P[1],0]-mat[ref_P[0],0])
            
        Cdmin = min(mat[:,2])
        ClCdmax = max(mat[:,1]/mat[:,2])
        
        if Cla0 > 0 and ClCdmax < 1000:
            Clmax, AoA_Clmax = find_Clmax(mat[:,1],mat[:,0])
            Chara = [Cl0, Cla0, Clmax, AoA_Clmax, Cm0, Cma0, Cdmin, ClCdmax]
#            print(Chara)
        else:
            Chara=[]
    else:
        Chara=[]
    
    return Chara

def Get_Clmax(filedirect):
    
    ## Read File ##
    # =========== #
    # Read file and collect the aerodynamic data
    # Open file with 'r' - Read only
    f=open(filedirect,'r')
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
                        vars()[label[k]].append(temp[j])
                    else:
                        vars()[label[k]].append(temp[j])
                        k=k+1
                    j=j+1
        if not line:
            break    
    f.close()      
    
    ## Calculate Aerodynamic Characteristics ##
    # ======================================= #
    # Save the infomations at matrix
    # Initialize the matrix        
    mat=zeros([len(vars()[label[0]]),len(label)])
    # mat label
    # AoA, Cl, Cd, Cdp, Cm, Top Xtr, Bot Xtr
    #   0,  1,  2,   3,  4,       5,       6
    
    # Record labels
    for i in range(0,len(label),1):
        mat[:,i]=vars()[label[i]]
    
    # Only calculate ADC if over the number of criteria AoA cases are analyzed
    if shape(mat)[0] > 0:
        Clmax, AoA_Clmax = find_Clmax(mat[:,1],mat[:,0])
        
        Updated_chara = [Clmax, AoA_Clmax]
    else:
        Updated_chara = []

    return Updated_chara

if __name__=='__main__':
    import os, sys
    direct_work=os.getcwd()
    
    # Find Code Directory
    direct_code=os.path.dirname(os.path.realpath(__file__))
    # If the code directory is not in PATH, add directory to import function
    if direct_code not in sys.path:
        sys.path.append(direct_code)
        
    direct_DB=os.path.join(direct_code,"DB")
    direct_tempDB = os.path.join(direct_DB,"Temp")

    i=6
    
    name_aerofile='Temp analyzed'+'_'+str(8)+'.txt'
    direct_file=os.path.join(direct_tempDB,name_aerofile)
    chara=Get_Clmax(direct_file)