# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 03:29:45 2021

@author: 218019067
"""

import os
import numpy as np
from ModeID import ModeID

class SystemID:
    # parameter ID for all extension modes
    def __init__(self, lbd, ubd):
        self.root_dir = "./Data/USV/"
        
        self.lower_bound = lbd   # lower bounds: m1, m2, m3, d1, d2, d3
        self.upper_bound = ubd   # upper bounds: m1, m2, m3, d1, d2, d3
        
    def ID(self, acc_digit): # main function
        if not self.readConfig():
            # find all modes
            self.findAllModes()
            
            # mode ID
            self.modeIDers = []
            for e_dir in self.extension_dirs:
                self.modeIDers.append(ModeID(e_dir, self.lower_bound, self.upper_bound))
            
            self.extension = []
            self.config = []
            for modeID in self.modeIDers:
                modeID.ID(acc_digit)
                self.extension.append(modeID.extension)
                self.config.append(modeID.config)
                
            self.config = list(map(list, zip(*self.config))) # transpose
            
            # each parameter fit
            self.fit_coef = []
            self.fit_func = []
            for conf in self.config:
                coef = np.polyfit(self.extension, self.config,self.dimension)
                self.fit_coef.append(coef)
                self.fit_func.append(np.poly1d(coef))
            
            # write to file
            np.savetxt("./Configurations/SystemID.csv", self.fit_coef, delimiter=",")
    
    def readConfig(self):
        # whether file exists
        config_file = "./Configurations/SystemID.csv"
        if os.path.exists(config_file):
            self.fit_coef = np.loadtxt(config_file, delimiter=",")
            self.fit_func = []
            for coef in self.fit_coef:
                self.fit_func.append(np.poly1d(coef))
            print("Succeed to read SystemID.csv!")
            return True
        # accuracy, known range of the min point in file
        else:
            return False
    
    def findAllModes(self):
        # 
        self.extension_dirs = []
        for ext_dir in os.listdir(self.root_dir):
             self.extension_dirs.append(self.root_dir + ext_dir + "/")
             
        self.dimension = len(self.extension_dirs)
    
    
# Test script
if __name__ == "__main__":
    lbd = [30., 30., 70., 1., 3., 2.]
    ubd = [60., 60., 150., 50., 40., 60.]
    systemID = SystemID(lbd, ubd)
    systemID.ID(0.01)