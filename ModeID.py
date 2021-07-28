# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 10:43:53 2021

@author: 218019067
"""

import os
import time
import math
import numpy as np
from matplotlib import pyplot as plt
import random
from Episode import Episode
import matlab.engine


class ModeID:
    # ID for one extension mode
    def __init__(self, root_dir, lbd, ubd):
        self.episode = Episode(root_dir)
        self.extension = int(root_dir.split("/")[3].split("_")[1]) # extension length
        self.N_para = 6 # Number of parameters
        #
        self.setBound(lbd, ubd)
        self.error_lst = []
    
    def setBound(self,lbd, ubd):
        self.lower_bound = np.array(lbd)   # lower bounds: m1, m2, m3, d1, d2, d3
        self.upper_bound = np.array(ubd)   # upper bounds: m1, m2, m3, d1, d2, d3
    
    def readConfig(self):
        # whether file exists
        config_file = "./Configurations/Extension_" + str(self.extension) + ".csv"
        if os.path.exists(config_file):
            self.config = np.loadtxt(config_file, delimiter=",")
            print("Succeed to read Extension_" + str(self.extension) + "!")
            return True
        # accuracy, known range of the min point in file
        else:
            return False
        
    def stepError(self, cur_lbd, cur_ubd, step, err_min = float('Inf')): # current lower bound, current upper bound, current step
        # for brute-force search: find the minimum configuration and the error
        
        configs = [] # for each parameter, make a range list
        for j in range(self.N_para):
            config_lst = np.arange(cur_lbd[j], cur_ubd[j]+step, step)
            configs.append(config_lst)
        #print(configs)
        
        t1 = time.time()
        for m1 in configs[0]:
            for m2 in configs[1]:
                for m3 in configs[2]:
                    for d1 in configs[3]:
                        for d2 in configs[4]:
                            for d3 in configs[5]:
                                c = np.array([m1, m2, m3, d1, d2, d3])
                                print("C: ", c)
                                err = self.f(c) # get error
                                if err <= err_min:
                                    self.config = c
                                    err_min = err
                                self.error_lst.append(err_min)
                                print("| Try config: ", self.config, " | Error: ", err_min)
        t2 = time.time()
        
        print("| Time: ", t2-t1)
        #print("Current config: ", self.config)
        #print("Error: ", err_min)
        #print("Time: ", t2-t1)
        #
        return err_min 
    
    def BFsearch(self, acc_digit): # units digit: 1, tenth digit:0.1
        # brute-force search
        
        print("+++++++ Brute-Force Search Method ++++++++")
        print("----------------------------------------")
        
        digit = int(math.log10(acc_digit))
        if digit >= 0: # if before the decimal point >=1
            accuracy = range(-digit, -digit+1)
        else: # if after the decimal point < 1
            accuracy = range(-digit+1)
        
        N = 6    # Number of parameters
        self.config = np.array([(i+j)/2 for i,j in zip(self.lower_bound, self.upper_bound)])  # start point is the middle
        print(self.config)
        print("| Objective accuracy: ", accuracy, " | Start point: ", self.config)
        cl = self.lower_bound       # current lower bound
        cu = self.upper_bound       # current upper bound
        
        err_min = float('Inf')
        
        # Linear search
        for i in accuracy: # each accuracy
            t_s = time.time()
            
            step = 10**(-i)
            err_min = self.stepError(cl, cu, step, err_min)
            
            for j in range(N):
                cl[j] = self.config[j] - step
                cu[j] = self.config[j] + step
    
            t_e = time.time()
            
            print("| Iteration: ", i, " | Current config: ", self.config)
            print("| Current error: ", err_min, " | Time consumption: ", t_e - t_s)
            print("| Current lowerbound: ", cl, " | Current upperbound: ", cu)
        # save to variables
        return err_min
    
    def GDsearch(self, e = 10**(-5)): # accuracy
        # GD method
        # Stopping criterion (for one search): 
        # Distance between two steps are short enough to converge
        # To stop searching and return the result:
        # Two consecutive searches converge to the same place
        # (points which are close enough)
        # Every search starts from a random point inside [lbd, ubd]
                
        config_prev = np.zeros(self.N_para)
        i = 0
        print("+++++++ Gradient Descent Method ++++++++")
        print("----------------------------------------")
        while True:
            i += 1
            if i > 1:
                config_prev = self.config  # store the previous result before random again
    
            self.config = self.configInit()  # start point
            print("| Iteration ", i, " | Start point: ", self.config)
            # print("Start point: ", config)
            # Backtracking parameters
            alpha = 0.5
            beta = 0.5
    
            # Gradient Descent
            x = self.config
            j = 0
            while True:
                j += 1
                # store current value of error
                err = self.f(x)
                self.error_lst.append(err)
                # Descent direction
                d = - getGradient(self.f, x)
                print("| Step: ", j, " | d: ", d)
                # Backtracking line search
                t = 1
                while (self.f(self.config + t * d) > self.f(self.config) + alpha * t * (-d) * d).all():
                    t = beta * t
            
                x_next = x + t * d
                for k in range(6):
                    if x_next[k] < self.lower_bound[k]:
                        x_next[k] = self.lower_bound[k]
                    elif x_next[k] > self.upper_bound[k]:
                        x_next[k] = self.upper_bound[k]
    
                # Stopping criterion
                if np.linalg.norm(x_next - x) < e:
                    break
    
                x = x_next  # Update for next iteration
                print("| t: ", t)
                print("| Next point: ", x)
    
            self.config = x
            err_min = self.f(self.config)
            print("End point: ", self.config, "\nError: ", err_min)
            print("------------------------------------------------")
    
            # Make sure the result is inside lbd and ubd
            if (self.config - self.lower_bound < 0).any() or (self.upper_bound - self.config < 0).any():
                print("Searching result outside from the required scope!!")
                print("Get config: ", self.config)
                print("Continue to next iteration...")
                continue
    
            # Stop searching
            if i > 1 and np.linalg.norm(self.config - config_prev) < e:
                print("--------- End Iteration ------------")
                return err_min
    
    def TRRsearch(self):
        lb = matlab.double(list(self.lower_bound))
        ub = matlab.double(list(self.upper_bound))

        eng = matlab.engine.start_matlab()
        rslt = eng.TRR_Solver(lb, ub)
        config = np.array(rslt[0][0:6])
        err_min = np.array(rslt[0][6])

        return config, err_min

    def configInit(self):
        # Generate 6 random configs, return in a np array
        c = np.array([])
        for idx in range(6):
            rand_num = self.lower_bound[idx] + random.random() * (self.upper_bound[idx] - self.lower_bound[idx])
            c = np.append(c, rand_num)
        return c
    
    def f(self, config):  # get error
        config = np.array(config)
        self.episode.setParameters(config.tolist())
        self.episode.run()
        return self.episode.error
    
    def ID(self, acc_digit): # main function
        # check whether config file exists
        #if not self.readConfig():
        if True:
            #self.GDsearch(acc_digit)
            # self.GDsearch()
            # t1 = time.time()
            c, e = self.TRRsearch()
            # e = self.BFsearch(acc_digit)
            self.config = c
            # print("config: ", c)
            print("config: ", self.config)
            print("error: ", e)
            # t2 = time.time()
            # print("Used time: ", t2-t1)
            # save to configuration file
            # np.savetxt("./Configurations/Extension_" + str(self.extension) + ".csv", self.config, delimiter=",")

    def showFigures(self):
        L = len(self.error_lst)
        x = list(range(1, L+1))
        plt.plot(x, self.error_lst)
        plt.show()
        
        
def f(config):  # get error
    config = np.array(config)
    root_dir = "./Data/USV/"
    ext_dir = ["Extension_0/", "Extension_10/", "Extension_20/", "Extension_30/", "Extension_40/", "Extension_50/"]
    episode = Episode(root_dir + ext_dir[0])
    episode.setParameters(config.tolist())
    episode.run()
    return episode.error

def getGradient(func, x):
    # Calculate gradient at point x by differencing
    x = np.array(x)
    delta = 0.01
    N = 6
    grad_lst = np.zeros(N)
    for i in range(N):
        delta_x = np.zeros(N)
        delta_x[i] = delta
        f1 = func(x - delta_x)
        f2 = func(x + delta_x)
        grad = (f2 - f1) / (2 * delta)
        grad_lst[i] = grad
    return grad_lst

def getHessian(func, x):
    # Calculate the Hessain matrix
    x = np.array(x)
    delta = 0.01
    N = 6
    hessian = np.zeros((N, N))
    for i in range(N):
        delta_x = np.zeros(N)
        delta_x[i] = delta
        f1 = getGradient(func, x-delta_x)
        f2 = getGradient(func, x+delta_x)
        h_row = (f2 - f1) / (2 * delta)
        hessian[i, :] = h_row
    return hessian


# Test script
if __name__ == "__main__":
    #
    root_dir = "./Data/USV/Extension_0/"
    
    lbd = [30., 30., 70., 1., 3., 2.]
    ubd = [60., 60., 100., 5., 4., 6.]
    modeID = ModeID(root_dir, lbd, ubd)
    modeID.ID(0.01)
    modeID.showFigures()
