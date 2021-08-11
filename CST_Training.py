# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 21:15:42 2018

@author: cck18
"""

"""
Info
=====
Training and Make Datafile
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time

direct_work=os.getcwd()
direct_code=os.path.dirname(os.path.realpath(__file__))

direct_DB=os.path.join(direct_code,"DB")
direct_input = os.path.join(direct_code,'Input')
Plotdirect=os.path.join(direct_code,"Plot")
sys.path.append(direct_code)

import CST_writeDB as writeDB
import CST_DB
import CST_ReadDB as ReadDB
import CST_Rinput as Rin
import CST_ANNv100 as AN
import CST_AssortData as AS
import CST_Log as Log
import CST_message as msg
import CST_exactClmax as exactClmax

# Setting is Xfoil setting
plt.close('all')
def Training(loop, Epoch, mini_batch_size, re_build):
    ##------------------------ Database Name Setting ------------------------##
    DBname_AF="CST Airfoil DB "+str(loop)+".txt"
    DBname_Total="CST Airfoil DB "+str(loop + 1)+".txt"
    
    DBname_Predict    = 'CST Prediction DB ' + str(loop) + '.txt'
    DBname_Predict_sorted    = 'CST Prediction DB_sorted ' + str(loop) + '.txt'
    
    DBname_Answer_raw = 'CST Answer DB_raw ' + str(loop) + '.txt' 
    DBname_Answer     = 'CST Answer DB ' + str(loop) + '.txt'
    DBname_predCACDB  = 'CST Prediction CAC DB ' + str(loop) + '.txt'
    
    DBname_Additional_raw = 'CST Additional DB_raw ' + str(loop) + '.txt'
    DBname_Additional_raw_Enhanced = 'CST Additional DB_raw_Enhanced ' + str(loop) + '.txt'
    DBname_Additional = 'CST Additional DB ' + str(loop) + '.txt'
    
    
    DBname_Error="CST Error DB "+str(loop)+".txt"
    Plotname = "Training Log "+str(loop)+".png"
    
    
    
    ##---------------------------- Training ANN -----------------------------##
    Log.log(None)
    message = 'Training Loop: ' + str(loop)
    msg.debuginfo(message)
    message = 'Start initialization for training ANN'
    msg.debuginfo(message)
    
    var, val = Rin.Rinput(direct_input,'input.txt',2) # 3 Hyperparameters of ANN
    no_output = int(val[3])
    
    start_time=time.time()
    
    ANN=AN.Build_networks(DBname_AF, loop)
    ANN.initialize_Training()
    ANN.initialize_ANN_Structure()
    # X: Aerodynamic Coeff. Y: Shape Parameters
    hist, X_testANS, Y_testANS, test_results = ANN.Training_ANN(Epoch)
    
    runtime = time.time() - start_time
    message = str("Runtime: {:d} sec = {:d} min".format(round(runtime),round(runtime/60)))    
    msg.debuginfo(message)
        
    ##---------------------------- Save Plot ----------------------------##
    
    if os.path.isfile(os.path.join(Plotdirect,Plotname)):
        os.remove(os.path.join(Plotdirect,Plotname))
    
    plt.figure(1)
    plt.legend(['Training','Test'])
    plt.title('Training Result: Loop {}'.format(loop))
    plt.savefig(os.path.join(Plotdirect,Plotname))
    
    
    message = 'Test Plot was Saved'        
    msg.debuginfo(message)
    
    if re_build == 1:   
        
        ##------------------ Predict Database Construction ------------------##
        # If Initial DB not exist in DB directory, It will make
        # If Initial DB exist, It will not run
        message = '>> Create CST Prediction DB'
        msg.debuginfo(message)
        
        if os.path.isfile(os.path.join(direct_DB,DBname_Predict)):
            os.remove(os.path.join(direct_DB,DBname_Predict))
        
        # Make Prediced Configuration DataBase
        writeDB.Config_DB(DBname_Predict,test_results)
        
        CST_DB.ConfigSort(DBname_Predict, DBname_Predict_sorted)
        
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Predict)))
    
        ##--------------------- Create Answer Database ----------------------##
        # If Additional DB not exist in DB directory, It will make
        # If Additional DB exist, It will not run
        msg.debuginfo('>> Create CST Answer DB')
        
        if os.path.isfile(os.path.join(direct_DB,DBname_Answer_raw)):
            os.remove(os.path.join(direct_DB,DBname_Answer_raw))
        
        dataset = np.append(Y_testANS, X_testANS,axis=1)
        msg.debuginfo(str('answer dataset size: {}'.format(np.shape(dataset))))
        msg.debuginfo(str('type of dataset: {}'.format(type(dataset))))
        
        # Make Answer DataBase
        writeDB.CSTDB(DBname_Answer_raw,dataset)
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Answer)))
    
        ##----------- Create Configure and Air Condition Database -----------##
        # If Additional DB not exist in DB directory, It will make
        # If Additional DB exist, It will not run
        msg.debuginfo('>> Create Configure and Air Condition DB')

        # Make CACDB
        CST_DB.Predict_Config2CACDB(DBname_Predict_sorted, DBname_Answer_raw, DBname_predCACDB)
        
        ##------- Run XFOIL with Configura and Air Condition Database -------##
        CST_DB.CAC2AFDB(loop, DBname_predCACDB, DBname_Additional_raw)
        exactClmax.UpdateDB_Clmax(loop, DBname_Additional_raw, DBname_Additional_raw_Enhanced)
#        CST_DB.AFDB_Postprocessing(loop,case = 1)
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Additional_raw_Enhanced)))

        ##-------------------- Assort Addtional Database --------------------##
        AF_DB=ReadDB.Read(DBname_AF)
        AddDB_raw, PrdDB, AnsDB = AS.run(DBname_Answer_raw, DBname_predCACDB, DBname_Additional_raw_Enhanced)
        
        ##--------------------- Create Answer DB Again ----------------------##
        # If Additional DB not exist in DB directory, It will make
        # If Additional DB exist, It will not run
        msg.debuginfo('>> Create Answer DB')
        
        if os.path.isfile(os.path.join(direct_DB,DBname_Answer)):
            os.remove(os.path.join(direct_DB,DBname_Answer))
            
        msg.debuginfo(str('answer dataset size: {}'.format(np.shape(dataset))))
        msg.debuginfo(str('type of dataset: {}'.format(type(dataset))))
        # Make Answer DataBase
        writeDB.CSTDB(DBname_Answer,AnsDB)
        
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Answer)))
        
        ##---------------------- Error Database ---------------------##
        if os.path.isfile(os.path.join(direct_DB,DBname_Error)):
            os.remove(os.path.join(direct_DB,DBname_Error))
        
        ErrDB = np.subtract(AddDB_raw, AnsDB)
        
        writeDB.CSTDB(DBname_Error,ErrDB)
        
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Error)))
        
        ##----------- Postprocessing Additional Database ------------##
        CST_DB.AFDB_Postprocessing(loop,DBname_Additional_raw_Enhanced, DBname_Additional)
        
        ##------------------- Intergrate Database -------------------##
        msg.debuginfo('>> Create Total DB')
        
        if os.path.isfile(os.path.join(direct_DB,DBname_Total)):
            os.remove(os.path.join(direct_DB,DBname_Total))
        
        AddDB = ReadDB.Read(DBname_Additional)
        # Make Total DB
        TotalDB=np.append(AF_DB,AddDB,axis=0)
        
        writeDB.CSTDB(DBname_Total,TotalDB)
        msg.debuginfo(str('File "{}" Created\n'.format(DBname_Total)))
        
        runtime = time.time() - start_time
        msg.debuginfo(str("Runtime: {:d} sec = {:d} min".format(round(runtime),round(runtime/60))))
        msg.debuginfo('>> Training Process Finished <<\n')
        
    #----------------- Training Information ------------------##
    DBname_Info="Training Info "+ str(loop)+".txt"
    filedirect=os.path.join(direct_DB,DBname_Info)    
    if os.path.isfile(filedirect):
        os.remove(os.path.join(direct_DB,DBname_Info))
    message = ('Create Training Info DB as "{}"'.format(DBname_Info))
    msg.debuginfo(message)
    
    f=open(filedirect,'w')
    f.write('Training Information\n')
    
    i_index = 0
    f.write('{:>10s}'.format('Epoch'))
    for i_index in range(len(hist.columns)):
        f.write('{:>10s}'.format(hist.columns[i_index]))
    f.write('\n')
    
    doubleline = ' ========='
    i_index = 0
    f.write('{:>10s}'.format(doubleline))
    for i_index in range(len(hist.columns)):
        f.write('{:>10s}'.format(doubleline))
    f.write('\n')
                
    i=0
    for i in range(len(hist.index)):
        j = 0
        f.write('{:>10d}'.format(hist.index[i]+1))
        for j in range(len(hist.columns)):
            f.write(' {:9f}'.format(hist.iloc[i,j]))
        f.write('\n')
        
    
    f.close()
    return hist
    
if __name__ == "__main__":
    hist = Training(1,100,10000,1)
    print(hist)
    