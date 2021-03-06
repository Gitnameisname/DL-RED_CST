# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 13:13:58 2018

@author: K-AI_LAB
"""

"""
Info
=====
Make CST curve airfoil
Based on ryanbarr's code
"""

# Description : Create a set of airfoil coordinates using CST parametrization method
# Input  : wl = CST weight of lower surface
#          wu = CST weight of upper surface
#          dz = trailing edge thickness
# Output : coord = set of x-y coordinates of airfoil generated by CST
#
# Adapted from:
#           Airfoil generation using CST parameterization method
#           by Pramudita Satria Palar
#           17 Jun 2013
#           http://www.mathworks.com/matlabcentral/fileexchange/42239-airfoil-generation-using-cst-parameterization-method

from numpy import zeros, ones, where, concatenate
from numpy import abs as npabs
from math import pi, cos, factorial, sqrt, acos, degrees

import matplotlib.pyplot as plt

from os import getcwd
from os import path as ospath
from sys import path as syspath

direct_work=getcwd()
direct_code=ospath.dirname(ospath.realpath(__file__))
syspath.append(direct_code)

class CST_shape(object):
    def __init__(self,N1=0.5, N2=1.0, wl=[-1, -1, -1, -1], wu=[1, 1, 1, 1], dz=0, N=200 ):
        # N1 and N2 parameters (N1 = 0.5 and N2 = 1 for airfoil shape)
        self.wl = wl
        self.wu = wu
        self.dz = dz
        self.N1 = N1
        self.N2 = N2
        self.N = N
        self.coordinate = zeros(N)

    def airfoil_coor(self, tempAF_name = ''):
        wl = self.wl
        wu = self.wu
        dz = self.dz
        N = self.N

        # Create x coordinate
        x = ones((N, 1))
        y = zeros((N, 1))
        zeta = zeros((N, 1))


        for i in range(0, N):
            zeta[i] = 2 * pi / N * i
            x[i] = 0.5*(cos(zeta[i])+1)

        center_loc = where(x == 0)  # Used to separate upper and lower surfaces
        center_loc = center_loc[0][0]

        xu = zeros(center_loc)
        xl = zeros(N-center_loc)

        for i in range(len(xl)):
            xu[i] = x[i]            # Upper surface x-coordinates
        for i in range(len(xu)):
            xl[i] = x[i + center_loc]   # Lower surface x-coordinates

        yl = self.__ClassShape(wl, xl, -dz) # Call ClassShape function to determine lower surface y-coordinates
        yu = self.__ClassShape(wu, xu, dz)  # Call ClassShape function to determine upper surface y-coordinates

        y = concatenate([yu, yl])  # Combine upper and lower y coordinates

        self.coord = [x, y]  # Combine x and y into single output

#        self.plotting()
        if len(tempAF_name) > 0:
            self.__writeToFile(x, y, tempAF_name)
            
        return self.coord

    # Function to calculate class and shape function
    def __ClassShape(self, w, x, dz):

        # Class function; taking input of N1 and N2
        C = zeros(len(x))
        for i in range(len(x)):
            C[i] = x[i]**self.N1*((1-x[i])**self.N2)

        # Shape function; using Bernstein Polynomials
        n = len(w) - 1  # Order of Bernstein polynomials

        K = zeros(n+1)
        for i in range(0, n+1):
            K[i] = factorial(n)/(factorial(i)*(factorial((n)-(i))))

        S = zeros(len(x))
        for i in range(len(x)):
            S[i] = 0
            for j in range(0, n+1):
                S[i] += w[j]*K[j]*x[i]**(j) * ((1-x[i])**(n-(j)))

        # Calculate y output
        y = zeros(len(x))
        for i in range(len(y)):
            y[i] = C[i] * S[i] + x[i] * dz

        return y

    def __writeToFile(self, x, y, tempAF_name):

        direct_save = ospath.join(direct_code,'DB','Temp')
        
        # tempAF_name??? .txt ??????????????? ????????? ?????????.
        direct_file = ospath.join(direct_save, tempAF_name)

        f = open(direct_file, 'w')
        f.write("Temp Airfoil\n")
        for i in range(len(x)):
            f.write('{:10.5f}{:10.5f}\n'.format(float(x[i]), float(y[i])))
        f.close()
        
    def getVar(self):
        return self.wl, self.wu

    def plotting(self, no_core, no_line):
        plt.close()
        direct_plot = ospath.join(direct_code,'DB','Temp','plot')
        Plotname = str(int(no_core))+'_'+str(int(no_line))+'.png'
        x_coor = self.coord[0]
        y_coor = self.coord[1]
        for i in range(len(x_coor)):
            if npabs(x_coor[i]) < 0.000001:
                center = i

        fig = plt.figure(no_core+1)
        plt.plot(x_coor[0:center], y_coor[0:center],label='upper')
        plt.plot(x_coor[center:], y_coor[center:],label='lower')
        plt.xlabel('x/c')
        plt.ylabel('y/c')
        plt.xlim(xmin=-0.1, xmax=1.1)
        plt.ylim(ymin=-0.6, ymax=0.6)
        plt.legend()
#        plt.spines['right'].set_visible(False)
#        plt.spines['top'].set_visible(False)
#        plt.yaxis.set_ticks_position('left')
#        plt.xaxis.set_ticks_position('bottom')
        plt.grid(True)
#        plt.show()
        plt.savefig(ospath.join(direct_plot,Plotname))
        plt.close()
        
class CST_shape_preproc(object):
    def __init__(self,N1=0.5, N2=1.0, wl=[-1, -1, -1, -1], wu=[1, 1, 1, 1], dz=0, N=200 ):
        # N1 and N2 parameters (N1 = 0.5 and N2 = 1 for airfoil shape)
        self.wl = wl
        self.wu = wu
        self.dz = dz
        self.N1 = N1
        self.N2 = N2
        self.N = N
        self.coordinate = zeros(N)

    def airfoil_coor(self):
        wl = self.wl
        wu = self.wu
        dz = self.dz
        N = self.N

        # Create x coordinate
        x = ones((N, 1))
        zeta = zeros((N, 1))


        for i in range(0, N):
            zeta[i] = 2 * pi / N * i
            x[i] = 0.5*(cos(zeta[i])+1)

        center_loc = where(x == 0)  # Used to separate upper and lower surfaces
        center_loc = center_loc[0][0]

        xu = zeros(center_loc)
        xl = zeros(N-center_loc)

        for i in range(len(xl)):
            xu[i] = x[i]            # Upper surface x-coordinates
        for i in range(len(xu)):
            xl[i] = x[i + center_loc]   # Lower surface x-coordinates

        yl = self.__ClassShape(wl, xl, -dz) # Call ClassShape function to determine lower surface y-coordinates
        yu = self.__ClassShape(wu, xu, dz)  # Call ClassShape function to determine upper surface y-coordinates

        side1 = sqrt((xu[-1]-xl[0])**2+(yu[-1]-yl[0])**2)
        side2 = sqrt((xl[1]-xl[0])**2+(yl[1]-yl[0])**2)
        side3 = sqrt((xu[-1]-xl[1])**2+(yu[-1]-yl[1])**2)
        
        cos3 = (side1**2 + side2**2 - side3**2)/(2*side1*side2)
        # decision = 1 : remain
        # decision = 0 : remove
        if cos3 > 1 or cos3 < -1:
            decision = 0
        else:
            angle3 = degrees(acos(cos3))
            
            if angle3 > 160:
                decision = 1
            else:
                decision = 0

        return angle3, decision

    # Function to calculate class and shape function
    def __ClassShape(self, w, x, dz):

        # Class function; taking input of N1 and N2
        C = zeros(len(x))
        for i in range(len(x)):
            C[i] = x[i]**self.N1*((1-x[i])**self.N2)

        # Shape function; using Bernstein Polynomials
        n = len(w) - 1  # Order of Bernstein polynomials

        K = zeros(n+1)
        for i in range(0, n+1):
            K[i] = factorial(n)/(factorial(i)*(factorial((n)-(i))))

        S = zeros(len(x))
        for i in range(len(x)):
            S[i] = 0
            for j in range(0, n+1):
                S[i] += w[j]*K[j]*x[i]**(j) * ((1-x[i])**(n-(j)))

        # Calculate y output
        y = zeros(len(x))
        for i in range(len(y)):
            y[i] = C[i] * S[i] + x[i] * dz

        return y

if __name__ == '__main__':
    #wl = [-0.40000, -0.40000, -0.40000, -0.40000]
    #wu = [0.00000, 0.00000,   0.00000,  -0.40000]
    wu = [-0.00107, 0.00094, -0.01037, 0.03574]      # Upper surface
    wl = [-0.00429, 0.02677, -0.00542, 0.00053]    # Lower surface
    dz = 0.
    N = 200

    airfoil_CST = CST_shape(0.5, 1.0, wl, wu, dz, N)
    coord = airfoil_CST.airfoil_coor(0,0)
    airfoil_CST.plotting()
    thick = []
    j = 0
    for j in range(99):
        thick.append(coord[1][j+1]-coord[1][199-j])
    thick_max = max(thick)
