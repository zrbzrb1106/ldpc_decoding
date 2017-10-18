# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:06:50 2017

@author: renbi
"""

#import sum_product as sp
import numpy as np
import generate_matrix as gm
import sum_product as sp


L = 150
ms = 2
K = 2
J = 1

winSize = 3
winIndex = 0
codex = 0
res = 0

code_len = K * L

#generate random received code
def gen_code(code_len):

    e = 0.2 #bit flipping prob.
    y1 = np.log(e/(1-e))
    y0 = np.log((1-e)/e)

    len = code_len
    code = np.zeros([1, len])
    rand_index = np.array([], dtype = 'int')
    temp = -1
    
#    code = np.zeros([1, len])
    while(1):
        rand = np.random.randint(0, len)
        if rand in rand_index:
            continue
        temp = rand
        rand_index = np.append(rand_index, temp)
        if rand_index.size == int(np.ceil(e * len)):
            break
    
    for i in rand_index:
        code[0][i] = 1
    
    for index, j in enumerate(code[0]):
        if j == 0:
            code[0][index] = y0
        else:
            code[0][index] = y1
        
    return code

codex = gen_code(code_len)


#generate the matrix for windowed decoding
H = np.matrix(gm.generate_matrix(L, K, J, ms))

#decoded result of last decoding
code_before = codex[0][winIndex:winIndex + (2*winSize)]

#'''L - winSize'''
#initializing the final result
result = np.zeros([1, code_len])
# main part of windowed decoding
while(winIndex <= L - winSize ):
    # current input code
    curr_code = codex[0][2*winIndex:2 *winIndex + (2*winSize)]
    
    print(curr_code)
    # current window
    currWin = H[winIndex:(winIndex+ms+1), 2*winIndex:(2*winIndex + 2*winSize)]
#    print(currWin)
    
    res = sp.ldpc_soft_decision(currWin, curr_code, code_before)
    result[0][2*winIndex:(2*winIndex + 2*winSize)] = res
    
    # give the result to the next step of decoding
    code_before = res
    
#    print(codex)
#    print("res...............", res)
    # move the window
    winIndex += 1

#for better present
codex[codex > 0] = 0
codex[codex < 0] = 1
print(codex)
result[result > 0] = 0
result[result < 0] = 1
print(result)



#res = sp.ldpc_soft_decision(currWin, code_test)
#a, b = currWin.shape
#
#e = 0.2
## compute LLR
#y1 = np.log(e/(1-e))
#y0 = np.log((1-e)/e)
#
#print("*************************")
## get random test code
#rand = np.random.randint(0,b)
#array0 = np.array(np.zeros(b,int), dtype = 'float32')
#for j in array0:
#    array0[rand]=1
#print(array0)
##array0.dtype = 'float32'
#print(array0)
#for i in range(0,b):
#    if array0[i] == 0:
#        array0[i] = y0
#    else:
#        array0[i] = y1
#        
#code_test = array0
#
#print(code_test)

#res = sp.ldpc_soft_decision(currWin, code_test, code_begin)
#print("*************************")


