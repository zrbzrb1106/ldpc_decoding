# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 22:11:06 2017

@author: renbi
"""
import numpy as np

def generate_matrix(m_L, KK, JJ, msms):

    L = m_L
    ms = msms
    K = KK
    J = JJ

    rows = (L + ms) * J
    colums = L * K
    a = np.zeros((rows, colums)) 
    
    index = 0
    flag = 0
    flag4index = 0
    
    for i in range(colums):
        if flag4index == K:
            index += 1
            flag4index = 0
        for j in range(rows):
            if j >= index and j<=(index+ms) :
                a[j][i] = 1
                flag += 1
                if flag == ms + 1:
                    flag = 0
                    flag4index += 1
                    break
    return a