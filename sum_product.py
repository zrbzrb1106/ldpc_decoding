#!/usr/bin/env python
# -*- coding: utf-8 -*


#---------LDPC Example------------ #

import numpy as np
##
##a = array([[1,1,0,1,0,0],
##		   [0,1,1,0,1,0],
##		   [1,0,0,0,1,1],
##		   [0,0,1,1,0,1]])
#
#a = array([[1,1,0,0,0,0],
#		   [1,1,1,1,0,0],
#		   [1,1,1,1,1,1]])
#
#H = np.matrix(a)
#print(H)
#
#a, b = H.shape
#
#e = 0.2
## compute LLR
#y1 = np.log(e/(1-e))
#y0 = np.log((1-e)/e)
#
#print("*************************")
## get random test code
#rand = np.random.randint(0,b)
#array0 = np.array(np.zeros(b,int))
#for j in array0:
#    array0[rand]=1
#print(array0)
#
## test code in example
##array0 = np.array([1,0,1,0,1,1])
##print array0
#array0.dtype = 'float32'
##array0.dtype = 'float'
##print array0, generate R
#for i in range(0,b):
#    if array0[i] == 0:
#        array0[i] = y0
#    else:
#        array0[i] = y1
#code_test = array0
#print(code_test)
#print("*************************")


def ldpc_soft_decision(H, code_0, code_1):
    iter = 1
    # Initialization
    R = code_0
    R0 = code_1
#    print("now....", R)
#    print("before...", R0)
    n_c, n_v = H.shape
    M = np.matrix(np.zeros(shape = (n_c, n_v)))
    E = np.matrix(np.zeros(shape = (n_c, n_v)))
    B = []
    temp = []
#    L = R0
    L = np.zeros(n_v)
    c = np.zeros(n_v, int)
    for i in range(0, n_v):
        for j in range(0, n_c):
            if H[j,i] == 1:
                M[j,i] = R0[i]
    #print M
    # get B
    for j in range(0, n_c):
        for i in range(0, n_v):
            if H[j,i] == 1:
                temp.append(i)
        B.append(temp)
        temp = []
    #print B

    # iteration
    for r in range(0, iter):
		# generate E
        for j in range(0, n_c):
            for i in range(0, n_v):
                if H[j,i] != 0:
                    a = 1.0
                    for k in B[j]:
                        if k != i:
                            if(a - 0.999999 > 0):
                                a = 0.999999
                            a = a * np.tanh(M[j,k]/2)
#                    print("a.......................", a)
                    E[j,i] = np.log((1+a)/(1-a))
#        print(E)
		# generate hard decision
        for i in range(0, n_v):
            temp = 0
            for j in range(0, n_c):
                temp = temp + E[j,i]
            L[i] = 	R[i] + temp
            if L[i] <= 0:
                c[i] = 1
            else:
                c[i] = 0
		# stop requirements
        if np.all(np.array([x % 2 for x in np.array(np.dot(c, H.T)).flatten()]) == 0) or r == iter - 1:
            return L
            break
		# bit messages
        else:
            for i in range(0, n_v):
                for j in range(0, n_c):
                    if H[j,i] != 0:
                        M[j,i] = int(sum(E[:,i])) - E[j,i] + R[i]

#print(ldpc_soft_decision(H, code_test))
