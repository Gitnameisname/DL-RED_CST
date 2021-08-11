# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 20:23:58 2020

@author: CK_DL2
"""

""" 
본 코드는 CAC DB에서 해석에 적합하지 않는 형상을 걸러내기 위한 코드입니다.
CAC DB에서 형상 파라메터만 뽑아낸 뒤, 해당 형상의 앞전 세 개의 좌표가 이루는 내각의 합이 160도 이하이면 제거
                                                                                    160도 이상이면 유지
본 예시파일이 정상적으로 작동한다는 것을 확인하면, CST_DB 코드로 편입시킵니다.
"""

import numpy as np
import os, sys

direct_work=os.getcwd()
direct_code=os.path.dirname(os.path.realpath(__file__))
sys.path.append(direct_code)

import CST_ReadDB as RDB
import CST_AF

direct_DB = os.path.join(direct_code,'DB')

DBname_CACDBinit = 'CAC DB init 1.txt'
DBname_CACDBsorted = 'CAC DB sorted 1.txt'

# CAC DB를 읽습니다. #
CACDBinit = RDB.Read(DBname_CACDBinit, direct_DB)

num_AF = np.shape(CACDBinit)[0]
DB_CACsorted = np.zeros([0,10])

i=0

# 검사도 멀티스레드 적용해야것다 #

while i < num_AF:
    # CAC DB의 첫번째 열로부터 에어포일 정보를 읽습니다. #
    example_Airfoil = CACDBinit[i,:8]
    wl = example_Airfoil[:4]
    wu = example_Airfoil[4:8]
    
    # CAC DB의 첫번째 에어포일을 생성합니다.
    AF = CST_AF.CST_shape(wl=wl, wu=wu)
    coord = AF.airfoil_coor(0,1)
    
    # 해당 에어포일의 앞전 각도를 구합니다. #
    # decision이 1이 나오면 각도가 160도 이상입니다. #
    # Angle의 값과 이 값이 일치하는지 확인하십시오 #
    AF_Check = CST_AF.CST_shape_preproc(wl=wl, wu=wu)
    angle, decision = AF_Check.airfoil_coor()
    
    if decision == 1:
        DB_CACsorted = np.append(DB_CACsorted, np.expand_dims(CACDBinit[i,:],axis = 0), axis = 0)
        
    i += 1
    
    progress=('Progress: '+str(i)+'/'+str(num_AF))
    sys.stdout.write('\r'+progress)






