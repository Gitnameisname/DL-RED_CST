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
from sys import exit as sysexit
from os import path as ospath
from sys import path as syspath
import numpy as np
import matplotlib.pyplot as plt


direct_code=ospath.dirname(ospath.realpath('__file__'))
direct_DB=ospath.join(direct_code,"DB")
syspath.append(direct_code)

direct_Analyze=ospath.join(direct_code,'Analyzed DB')
direct_Input = ospath.join(direct_code,'Input')

import CST_ReadDB as RDB
import CST_Rinput as Rin
import CST_writeDB as wDB

# this function find the file with keyword, such as Answer, Error, etc.
# regardless of loop number.
def file_finder(list_files, type_file, DB_type):
    i=0
    key=-1
    for i in range(len(list_files)):
        decomp_list = (list_files[i].split(' '))
        if (type_file in decomp_list) and (DB_type in decomp_list):
            key = i
    if key >= 0:
        print(list_files[key])
        return key
    else:
        sysexit('Cannot find the file type: {}'.format(type_file))

def STD_cal(data):
    data_mean = np.mean(data,0)
    data_std  = np.std(data,0)
    
    return data_mean, data_std
    
def STD(name_inputfile):
    list_folder = Rin.Rinput(direct_Input, name_inputfile,1)[1]
    i=0
    for i in range(len(list_folder)):
        vars()['path_'+str(i)]=ospath.join(direct_Analyze,list_folder[i])
    
    type_file = 'Error'
    data = []
    i=0
    for i in range(len(list_folder)):
        list_files =os.listdir(vars()['path_'+str(i)])
        key = file_finder(list_files,type_file)
    
        data.append(RDB.Read(list_files[key], vars()['path_'+str(i)]))
        
    label = RDB.Read_datalist(list_files[key])
    statDB_mean = np.zeros([0,len(label)])
    statDB_std  = np.zeros([0,len(label)])
    
    i=0
    for i in range(len(list_folder)):
        mean, std = STD_cal(data[i])
        statDB_mean = np.append(statDB_mean, np.expand_dims(mean,0),0)
        statDB_std  = np.append(statDB_std, np.expand_dims(std,0),0)

def Get_Statistics():
    
    #######################################
    name_inputfile='DataAnalysis.txt'
    #######################################
    
    # Get names of folder which has data
    list_folder = Rin.Rinput(direct_Input, name_inputfile,1)[1]
    i=0
    for i in range(len(list_folder)):
        vars()['path_'+str(i)]=ospath.join(direct_Analyze,list_folder[i])
    
    type_file = ['Answer', 'Additional']
    Ansdata = []
    Adddata = []
    i=0
    for i in range(len(list_folder)):
        list_files =os.listdir(vars()['path_'+str(i)])
        key_Ans = file_finder(list_files,type_file[0],'DB')
        key_Add = file_finder(list_files,type_file[1],'DB_raw')
    
        Ansdata.append(RDB.Read(list_files[key_Ans], vars()['path_'+str(i)]))
        Adddata.append(RDB.Read(list_files[key_Add], vars()['path_'+str(i)]))
    
    Err = []
    i = 0
    for i in range(len(list_folder)):
        Err.append(Adddata[i]-Ansdata[i])
        
    label = RDB.Read_datalist(list_files[key_Ans])
    
    statDB_mean = np.zeros([0,len(label)])
    statDB_std  = np.zeros([0,len(label)])
    
    i=0
    for i in range(len(list_folder)):
        mean, std = STD_cal(Err[i])
        statDB_mean = np.append(statDB_mean, np.expand_dims(mean,0),0)
        statDB_std  = np.append(statDB_std, np.expand_dims(std,0),0)
        
    wDB.CST_stats(list_folder,str('Data Analysis_stat Mean.txt'),statDB_mean)
    wDB.CST_stats(list_folder,str('Data Analysis_stat STD.txt'),statDB_std)

def Percentile_Plot():
    
    #######################################
    name_inputfile='DataAnalysis.txt'
    #######################################
    
    list_folder = Rin.Rinput(direct_Input, name_inputfile,1)[1]
    i=0
    for i in range(len(list_folder)):
        vars()['path_'+str(i)]=ospath.join(direct_Analyze,list_folder[i])
    
    type_file = ['Answer', 'Additional','Error']
    Ansdata = []
    Adddata = []
    ABSErrdata = []
    
    i=0
    for i in range(len(list_folder)):
        list_files =os.listdir(vars()['path_'+str(i)])
        key_Ans = file_finder(list_files,type_file[0],'DB')
        key_Add = file_finder(list_files,type_file[1],'DB_raw')
        key_ABSErr = file_finder(list_files,type_file[2],'DB')
    
        Ansdata.append(RDB.Read(list_files[key_Ans], vars()['path_'+str(i)]))
        Adddata.append(RDB.Read(list_files[key_Add], vars()['path_'+str(i)]))
        ABSErrdata.append(RDB.Read(list_files[key_ABSErr], vars()['path_'+str(i)]))
        
    percentile = ['99%','95%','90%']
    percentile_index = np.zeros([len(list_folder),len(percentile)])
    # Get percentile indexes of each cases
    i=0
    for i in range(len(list_folder)):
        no_data = np.shape(ABSErrdata[i])[0]
        percentile_index[i,0] = int(np.round(no_data*0.01)) # 99%
        percentile_index[i,1] = int(np.round(no_data*0.05)) # 95%
        percentile_index[i,2] = int(np.round(no_data*0.10)) # 90%
    
    label = RDB.Read_datalist(list_files[key_Ans])
    percentile_value = np.zeros([len(list_folder),len(percentile),len(label)])
    
    i=0
    for i in range(len(list_folder)):
        j=0
        for j in range(len(label)):
            temp = np.copy(ABSErrdata[i][:,j])
            temp = temp[temp.argsort()[::-1]]
            percentile_value[i,0,j] = temp[int(percentile_index[i,0])]
            percentile_value[i,1,j] = temp[int(percentile_index[i,1])]
            percentile_value[i,2,j] = temp[int(percentile_index[i,2])]
            
    plt.close('all')
    plt.ioff()
    fig_size=[16,9]
    plt.rcParams["figure.figsize"]=fig_size
    list_Group = Rin.Rinput(direct_Input, name_inputfile,2)[1]
    list_Group_index=[]
    i=0
    for i in range(len(list_Group)):
        temp=[]
        list_Group[i] = list_Group[i].split(',')
        j=0
        for j in range(len(list_Group[i])):
            k=0
            for k in range(len(list_folder)):
                if list_folder[k]==list_Group[i][j]:
                    temp.append(k)
        list_Group_index.append(temp)
        
    i=0
    for i in range(len(list_Group)):
        j=0
        plt.close('all')
        
        for j in range(len(label)):
            fig=plt.figure(j)
            k=0
            for k in range(len(list_Group[i])):
                plt.bar(np.arange(len(percentile)) + (k-int(len(list_Group[i])/2)) * (1/(len(list_Group[i])+1)) ,percentile_value[list_Group_index[i][k],:,j], (1/(len(list_Group[i])+1)), label=list_Group[i][k])
                for a, b in zip(np.arange(len(percentile)) + (k-int(len(list_Group[i])/2)) * (1/(len(list_Group[i])+1)), percentile_value[list_Group_index[i][k],:,j]):
                    plt.text(a, b*1.02, '{:3.2E}'.format(b),fontsize=11,horizontalalignment='center')
            plt.legend(fontsize=18)
            plt.xticks(np.arange(len(percentile)), percentile)
            plt.tight_layout()
            plt.title('Percentile Rank: Group '+str(i+1)+'/'+str(len(list_Group))+', '+label[j],fontsize=28)
            plt.xlabel('Percentile Rank(from lower error)',fontsize=20)
            plt.ylabel('ABS Error',fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.tight_layout()
            
            direct_plot=os.path.join(direct_Analyze,'Plot')
            plt.savefig(os.path.join(direct_plot,'Percentile Rank_Group '+str(i+1)+'_'+label[j]))
            
if __name__=="__main__":
    Percentile_Plot()
            
