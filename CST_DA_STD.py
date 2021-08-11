# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 14:05:17 2018

@author: CK_DL2
"""

"""
Info
=====
Collecting the Result
Analyze the Result and Error
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

import CST_writeDB as wDB

def 

direct_Input=os.path.join(direct_code,"Analyzed DB")
direct_DBfolder=os.path.join(direct_code,"Analyzed DB",name_Hyperparameter)

_, loop = Rin.Rinput(direct_Input,name_inputfile,2)
loop = loop[0]

#
var, val = Rin.Rinput(direct_Input,name_inputfile,1)

i=0

name_DBfolder = val[i]
direct_DB =os.path.join(direct_DBfolder,name_DBfolder)
## To Extract Lable Name ##
name_AnsDB = 'Answer DB'+str(loop)+'.txt'
name_label = RDB.Read_datalist(name_AnsDB,direct_DB)
##=======================##
name_label[0] = 'Max Camber'
name_label[1] = 'Max Camber\nLocation'
name_label[2] = 'Max Thickness'

Err_meanDB = np.zeros([len(val),len(name_label)])
Err_stdDB = np.zeros([len(val),len(name_label)])

sigma = 6
i = 0

direct_Plotsave = os.path.join(direct_Plot,name_Hyperparameter)
try:
    if not os.path.exists(direct_Plotsave):
        os.makedirs(direct_Plotsave)
        
except OSError:
    print('Error occured: Creating folder')

while i < len(val):
    
    name_DBfolder = val[i]
    direct_DB =os.path.join(direct_DBfolder,name_DBfolder)
    
    name_AddDB = 'Additional DB'+loop+'.txt'
    name_AnsDB = 'Answer DB'+loop+'.txt'
    
    AddDB = RDB.Read(name_AddDB,direct_DB)
    AnsDB = RDB.Read(name_AnsDB,direct_DB)
    
    ErrDB = AddDB - AnsDB
    
    name_label[0] = 'Max Camber'
    name_label[1] = 'Max Camber Location'
    name_label[2] = 'Max Thickness'
    
    ## Normal Distribution ##
    
    j=0
    while j < len(name_label):
        
        Err_data=np.copy(ErrDB[:,j])
        Err_data.sort()
        Err_mean = np.mean(Err_data)
        Err_std = np.std(Err_data)
        
        Err_meanDB[i,j]=np.copy(Err_mean)
        Err_stdDB[i,j]=np.copy(Err_std)
        
        Err_normdist = stats.norm.pdf(Err_data, Err_mean, Err_std)
        
        plt.ioff()
        plt.figure(j)
        plt.grid(True)
        plt.plot(Err_data,Err_normdist,linewidth=3)
        plt.title('Normal Distribution\nLoop '+str(i)+': '+name_label[j], Fontsize = 16)
        plt.ticklabel_format(style='sci',axis='x',scilimits=(0,0))
        plt.xticks(Fontsize=12)
#        plt.xlim([-max(abs(Err_data)),max(abs(Err_data))])
        plt.xlim([-sigma*Err_std,sigma*Err_std])
        plt.xlabel(name_label[j],fontsize = 12)
        plt.yticks(Fontsize=12)
        
        
        j += 1
    
    print('Normal Distribution: Case {} finished'.format(i+1))
    i += 1

i=0
for i in range(len(name_label)):
    plt.figure(i)
    plt.legend(val,fontsize=14,loc='upper right')
    plt.savefig(os.path.join(direct_Plotsave,'Normal Distribution_'+name_label[i]))

plt.close('all')
i=0
while i < len(val):
    direct_Plotsave = os.path.join(direct_Plot,val[i])
    try:
        if not os.path.exists(direct_Plotsave):
            os.makedirs(direct_Plotsave)
            
    except OSError:
        print('Error occured: Creating folder')
    
    name_DBfolder = val[i]
    direct_DB =os.path.join(direct_DBfolder,name_DBfolder)
    
    name_AddDB = 'Additional DB'+loop+'.txt'
    name_AnsDB = 'Answer DB'+loop+'.txt'
    
    AddDB = RDB.Read(name_AddDB,direct_DB)
    AnsDB = RDB.Read(name_AnsDB,direct_DB)
    
    ErrDB = AddDB - AnsDB
    
    name_label[0] = 'Max Camber'
    name_label[1] = 'Max Camber Location'
    name_label[2] = 'Max Thickness'
    
    ## Normal Distribution ##
    
    j=0
    while j < len(name_label):
        
        Err_data=np.copy(ErrDB[:,j])
        Err_data.sort()
        Err_mean = np.mean(Err_data)
        Err_std = np.std(Err_data)
        
        Err_meanDB[i,j]=np.copy(Err_mean)
        Err_stdDB[i,j]=np.copy(Err_std)
        
        Err_normdist = stats.norm.pdf(Err_data, Err_mean, Err_std)
        
        Err_z = (Err_data - Err_mean)/Err_std
        Err_stdnormdist = stats.norm.pdf(Err_z, 0, 1)
        
        plt.ioff()
        plt.grid(True)
        plt.plot(Err_z,Err_stdnormdist,linewidth=3)
        plt.title('Standard Normal Distribution\nLoop '+str(i)+': '+name_label[j], Fontsize = 16)
        plt.xticks(Fontsize=12)
#        plt.xlim([-max(abs(Err_z)),max(abs(Err_z))])
        plt.xlim([-sigma,sigma])
        plt.xlabel('Z',Fontsize = 12)
        plt.yticks(Fontsize=12)
        plt.savefig(os.path.join(direct_Plotsave,'Standard Normal Distribution_Loop '+str(i)+'_'+name_label[j]))
        plt.close()
        
        
        j += 1
    
    print('Standard Normal Distribution: Case {} finished'.format(i+1))
    i += 1

wDB.NACADB_stats('Err_mean.txt',Err_meanDB)
wDB.NACADB_stats('Err_std.txt',Err_stdDB)