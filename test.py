# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 04:22:04 2021

@author: 218019067
"""
import numpy as np

l1 = [1,2,3,4,5,6]
l2 = [0,1,2,3,4,5]

np.savetxt("./Test.csv", l1, delimiter=",")


print((l1+l2)/2)
print([i - j for i,j in zip(l1,l2)])

error = np.array([])

a = np.append(l2,l1)


