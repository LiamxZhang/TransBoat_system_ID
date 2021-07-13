# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:30:56 2021

@author: 218019067

input: PWM signal and propulsion

output: coefficient of the thruster model
"""

import os
import csv
import numpy as np
from matplotlib import pyplot as plt
#from matplotlib.pyplot import MultipleLocator

class ThrusterModel:
    def __init__(self, num):
        self.thruster_num = num
        self.order = 30
        
        #
        self.Regression()
        
    def readCSV(self, file_lst):
        header = 1 # header row number
        del_s = 10 # the first 10 data
        del_t = 10 # the last 10 data
        lever = 2 # leverage number
        
        
        PWM_T_pair = dict()
        for file in file_lst:
            with open(file, newline='') as csv_f:
                f_reader = csv.reader(csv_f)
                row_i = 0 # counting the row
                for row in f_reader:
                    row_i += 1
                    if row_i <= header:  # skip the first line
                        continue
                    idx = (row_i-1) % 100
                    if idx <= del_s or idx > (100 - del_t): # skip the first 10 and last 10 data
                        continue
                    pwm = eval(row[1])
                    thrust = eval(row[2])/lever
                    if idx == del_s+1 and file == file_lst[0]:
                        PWM_T_pair[pwm] = []
                    # try:
                    PWM_T_pair[pwm].append(thrust)
                    # except:
                    #     print(pwm)
        return PWM_T_pair

    def getMeanError(self, pwm, PWM_T):
        if not isinstance(pwm, list):
            t = np.array(PWM_T[pwm])
            t_max = np.max(t)
            t_min = np.min(t)
            t_avg = np.average(t)
            t_std = np.std(t, ddof = 1)
        else:
            # t_max = np.array([])
            # t_min = np.array([])
            # t_avg = np.array([])
            t_max = []
            t_min = []
            t_avg = []
            t_std = []
            for p in pwm:
                t = np.array(PWM_T[p])
                # np.append(t_max, np.max(t))
                # np.append(t_min, np.min(t))
                # np.append(t_avg, np.average(t))
                t_max.append(np.max(t))
                t_min.append(np.min(t))
                t_avg.append(np.average(t))
                t_std.append(np.std(t, ddof = 1))
        return t_avg, t_min, t_max, t_std
    
    # error bar plot
    def drawErrorBar(self, pwm, PWM_T):
        t_avg, t_min, t_max, t_std = self.getMeanError(pwm, PWM_T)
        #t_err_min = np.array(t_avg) - np.array(t_min)
        #t_err_max = np.array(t_max) - np.array(t_avg)
        
#        if not isinstance(pwm, list):
#            y_err = [[t_err_min], [t_err_max]]
#        else:
#            y_err = [t_err_min, t_err_max]
        # print(y_err)
        # plt.scatter(pwm, t_info[0])
        # print(pwm)
        # print(t_avg)
        plt.errorbar(pwm, t_avg, yerr=t_std, fmt='o', capsize = 3)
    
    # box plot
    def drawBoxPlot(self, PWM_T, pwm_l, pwm_h):
        data = []
        for p in range(pwm_l, pwm_h+1):
            data.append(PWM_T[p])
        
        plt.boxplot(data, positions = range(pwm_l, pwm_h+1), showfliers=False)
        #plt.grid(linestyle="--", alpha=0.3)
        
    # scatter plot
    def drawAllData(self, PWM_T, pwm_l, pwm_h):
        # draw all data points and fit into a nonlinear relation
        t_total = []
        pwm_ax = []
        # points = 80
        for pwm in range(pwm_l, pwm_h+1):
            t_total.extend(PWM_T[pwm])
            pwm_ax.extend([pwm]*len(PWM_T[pwm]))
        
        plt.scatter(pwm_ax, t_total)
        
    def showFigures(self):
        # check whether the data was read
        if 'self.PWM_T' not in locals().keys():
            directory = "./Data/Thruster/"+str(self.thruster_num)
            file_name = [directory+"/12_3_1.csv", directory+"/12_3_2.csv", directory+"/12_3_3.csv"]
            self.PWM_T = self.readCSV(file_name)
        
        pwm_l = 43
        pwm_h = 138
        # draw boxplot
        self.drawBoxPlot(self.PWM_T, pwm_l, pwm_h)
        
        # draw fitting function
        pwm = range(pwm_l, pwm_h+1)
        fit_result = self.fit_func(pwm)
        plt.plot(pwm,fit_result,ls='--',c='red',label='fitting with third-degree polynomial')
        
        # set labels
        plt.xlabel("PWM")
        plt.ylabel("Thrust")
        
        # set ticks
        pwm_l = 40
        pwm_h = 140
        ax=plt.gca()
        ax.set_xticks(list(range(pwm_l, pwm_h+1, 10)))
        ax.set_xticklabels(list(range(pwm_l, pwm_h+1, 10)))
        #x_major_locator=MultipleLocator(10)
        #ax.xaxis.set_major_locator(x_major_locator)
        #plt.show()
        # draw fitting curves
        
    #
    def fit(self, PWM_T, pwm_l, pwm_h):
        # fit data
        t_total = []
        pwm_ax = []
        # points = 80
        for pwm in range(pwm_l, pwm_h+1):
            t_total.extend(PWM_T[pwm])
            pwm_ax.extend([pwm]*len(PWM_T[pwm]))
        # fit_coef = np.polyfit(pwm_ax, t_total, 3)
        # fit data
        self.fit_coef = np.polyfit(pwm_ax,t_total,self.order)
        self.fit_func = np.poly1d(self.fit_coef)
        #print(self.fit_coef)
        
        # write to file
        np.savetxt("./Configurations/Thruster" + str(self.thruster_num) + ".csv", self.fit_coef, delimiter=",")
        
        return self.fit_coef, self.fit_func
        
    # propulsion
    def propulsion(self, pwm):
        if pwm == 0:
            prop = 0
        else:
            prop = self.fit_func(pwm)
        return prop
    
    # main step
    def Regression(self):
        # check whether the parameter file exists
        config_file = "./Configurations/Thruster" + str(self.thruster_num) + ".csv"
        if os.path.exists(config_file):
            self.fit_coef = np.loadtxt(config_file, delimiter=",")
            self.fit_func = np.poly1d(self.fit_coef)
        else:
            directory = "./Data/Thruster/"+str(self.thruster_num)
            file_name = [directory+"/12_3_1.csv", directory+"/12_3_2.csv", directory+"/12_3_3.csv"]
            self.PWM_T = self.readCSV(file_name)
            # fitting
            pwm_l = 43
            pwm_h = 138
            self.fit(self.PWM_T, pwm_l, pwm_h)
        
# Test script
if __name__ == "__main__":    
    thruster = ThrusterModel(1)
    thruster.showFigures()
    thruster = ThrusterModel(2)
    thruster.showFigures()
    thruster = ThrusterModel(3)
    thruster.showFigures()
    thruster = ThrusterModel(4)
    thruster.showFigures()
    plt.show()
    #PWM_T_pair = thruster.readCSV(file_name)
    # plt.plot(thrust_lst)
    #thruster.drawErrorBar(pwm, PWM_T_pair)
    #thruster.drawBoxPlot(pwm, PWM_T_pair)
    #thruster.drawAllData(PWM_T_pair, 43, 138)
    #thruster.Regression()
    #thruster.showFigures()
    print(thruster.propulsion(90))
