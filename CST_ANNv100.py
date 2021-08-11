# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 12:24:51 2017

@author: K_LAB
"""

"""
Info
=====
Generate Fully Connected Neural Network(FCNN)
Training FCNN about CST airfoils
Used Layer Normalization
Used Mini-Batch

v99: Cost function Changed
 - MSE > MSE / (L2norm of AnsDB / Number of elements of AnsDB)

v100: The version of tensorflow changed, from 1.14 to 2.0
"""

import tensorflow as tf
#tf.debugging.set_log_device_placement(True)

from tensorflow import keras
from tensorflow.keras import layers
from pandas import DataFrame

import numpy as np
import time
from sklearn.model_selection import train_test_split
import os
import sys
import matplotlib.pyplot as plt
from math import log10

direct_code=os.path.dirname(os.path.realpath(__file__))
direct_DB=os.path.join(direct_code,"DB")
direct_input = os.path.join(direct_code,'Input')
sys.path.append(direct_code)

import CST_Rinput as Rin
import CST_ReadDB as ReadDB
import CST_message as msg

epoch_log = 1

class Build_networks():
    def __init__(self,DBname_AF,caseNO):
        # Name of Airfoil DB
        self.DBname_AF=DBname_AF
        
        ## Data Call ##
        # read Data Base
        self.Data = ReadDB.Read(self.DBname_AF)
        self.caseNO = caseNO
        
        ## Parameters ##
        var, val = Rin.Rinput(direct_input,'input.txt',2)
        self.L_rate = float(val[4])
        self.n_input = int(val[2])
        self.n_output = int(val[3])
        self.No_HL = int(val[0])
        self.No_Neuron = int(val[1])
        self.Active_function = val[5]
        self.dtype = val[6]

        
    def initialize_Training(self):
        
        # This function was deleted in tf 2.0
            # Reset Variable Before running
            # tf.reset_default_graph()
        # Instead of that, the function below was used to remove the old parameters
        
        # keras.backend.clear_session()
        
        # For Batch Normalization
        self.epsilon = 1e-5

        # step size for save and display
        self.SnD_step = 1

        ## Prepare Data ##
        # [Geo] is Output Data
        # [Aero] is Input Data
        self.Geo = self.Data[:,0:self.n_output]
        self.Aero = self.Data[:,self.n_output:]    
        
    def initialize_ANN_Structure(self):
        
        ## Prepare Data ##
        # Divide Dataset as a Training Data (75%) and Test Data (25%)
        # random_stata : Fix the Divide rule 
        #       (None - Divide method is always change when we run the code)
        self.X_train, self.X_test, self.y_train, self.y_test=train_test_split(self.Aero, self.Geo, random_state=0 ) # Change training/test size
#        self.X_train, self.X_valid, self.y_train, self.y_valid=train_test_split(self.X_train, self.y_train, random_state=0 ) # Change training/test size
        
        ## Normalize ##
        # Make [info_data] for Normalize about total Input data
        # Future Work:
        #   Makes a function that can choose the Normalization method
        self.X_train_avg=np.average(self.X_train, axis = 0)
        self.X_train_std=np.std(self.X_train, axis = 0)
        
        # Save the Normalized data #
        direct_save = os.path.join(direct_code,"saved")
        Name_Normfile = "Normalization " + str(self.caseNO) + ".txt"
        direct_Normfile = os.path.join(direct_save, Name_Normfile)
        
        if os.path.isfile(direct_Normfile):
            os.remove(direct_Normfile)
        f = open(direct_Normfile, 'w')
        f.write('# Normalization data #\n')
        f.write('#1 Data for Normalization of inputs\n')
        
        # write avg #
        f.write('Xdata avg:\t')
        for i in range(len(self.X_train_avg)):
            if i < len(self.X_train_avg) - 1:
                f.write('{}, '.format(self.X_train_avg[i]))
            elif i == len(self.X_train_avg) - 1:
                f.write('{}\n'.format(self.X_train_avg[i]))
        
        # write std #
        f.write('Xdata std:\t')
        for i in range(len(self.X_train_std)):
            if i < len(self.X_train_std) - 1:
                f.write('{}, '.format(self.X_train_std[i]))
            elif i == len(self.X_train_std) - 1:
                f.write('{}\n'.format(self.X_train_std[i]))

        f.write('$\n')
        f.close()
        
        self.L2norm_avg = np.linalg.norm(self.y_train,2)/(np.shape(self.y_train)[0]*np.shape(self.y_train)[1])
        ## ANN Structure ##
        # Set the number of neuron of each layer
        
        message = str('Data type: {}'.format(self.dtype))
        msg.debuginfo(message)
        # Define the number of each neuron
        model_shape = []
        for i in range(self.No_HL+1):
            if i == 0:
                model_shape.append(layers.Dense(self.No_Neuron, activation = self.Active_function, input_shape = [self.n_input]))
            elif i < self.No_HL:
                model_shape.append(layers.Dense(self.No_Neuron, activation = self.Active_function))
                
            elif i == self.No_HL:
                model_shape.append(layers.Dense(self.n_output))
        
        model = keras.Sequential(model_shape)
        optimizer = tf.keras.optimizers.Adam(learning_rate = self.L_rate)
        
        model.compile(loss='mse',optimizer = optimizer, metrics=['mae','mse'])
        
        return model

    # Normalize data
    # Generally, use it for Input data
    # [info_data] should have
    #   Average of Data, Minimum of Data, Maximum of Data, Number of Data label
    #   [Array, Array, Array, Array], and AVG, MIN, MAX, must have the value of each Label
    # [scale] is the scale of the Normalize
    def Normalize(self, x):
        data_avg=self.X_train_avg
        data_std=self.X_train_std
        Ndata=np.zeros(np.shape(x))
        # Normalize Calculation
        for ds in range(self.n_input):
            Ndata[:,ds]=(x[:,ds]-data_avg[ds])/data_std[ds]
        
        return Ndata
    
    def Training_ANN(self,epoch):
        tf.compat.v1.reset_default_graph()
        model = self.initialize_ANN_Structure()
        model.summary()
        
        NXtrain=self.Normalize(self.X_train)
        NXtest=self.Normalize(self.X_test)
        
        self.history = model.fit(NXtrain, self.y_train, epochs = epoch, validation_split = 0.2, verbose = 0, callbacks=[realtime_results()])
        
        name_model = 'saved\model ' + str(self.caseNO) + '_2.h5'
        model.save(name_model)
        
        self.hist = DataFrame(self.history.history)
        
        output = model(NXtest)
#        Result_test, self.y_test, self.X_test
       
        return self.hist, self.X_test, self.y_test, output
        
class realtime_results(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    
    ## list of logs
    # loss, mae, mse, val_loss, val_mae, val_mse
    SnD_step = 10
    if epoch == 0:
        print('Epoch: {}'.format(epoch+1), end='\n')
        self.loss = []
        self.train_mse = []
        self.val_mse = []
        
        self.loss.append(logs['loss'])
        self.train_mse.append(logs['mse'])
        self.val_mse.append(logs['val_mse'])
        
        plt.figure(1)
        plt.ion()
        plt.plot(epoch+1,log10(self.train_mse[-1]),color="dodgerblue")
        plt.plot(epoch+1,log10(self.val_mse[-1]),color='orange')
        plt.grid(True)
        plt.xlabel('Update Epoch')
        plt.ylabel('Cost - Log10(MSE)')
    #        plt.title('Loop'+str(self.caseNO))   
        #f1.show()
        plt.pause(0.00001)

        # record cost and No.training  every [save_step]
    elif (epoch+1) % SnD_step == 0 and not epoch == 0:
        print('Epoch: {}'.format(epoch+1), end='\n')
        self.loss.append(logs['loss'])
        self.train_mse.append(logs['mse'])
        self.val_mse.append(logs['val_mse'])
        
        plt.figure(1)
        plt.ion()
        plt.plot([epoch-SnD_step+1,epoch+1],[log10(self.train_mse[-2]),log10(self.train_mse[-1])],color="dodgerblue")
        plt.plot([epoch-SnD_step+1,epoch+1],[log10(self.val_mse[-2]),log10(self.val_mse[-1])],color="orange")
        plt.grid(True)
        #f1.show()
        plt.pause(0.00001)
            
if __name__=='__main__':
    plt.close('all')
    loop = 1
    DBname_AF="CST Airfoil DB "+str(loop)+".txt"
    Epoch = 10000
    mini_batch_size = 5000
    
    ANN=Build_networks(DBname_AF, loop)
    ANN.initialize_Training()
    model = ANN.initialize_ANN_Structure()
    model.summary()
    
    hist, X_testANS, Y_testANS, test_results = ANN.Training_ANN(100)
    
    model.summary()
    
#    cost_train, cost_val, training_iter, result_test, ans, ans_aero = ANN.Training_ANN(Epoch,mini_batch_size)