# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 22:53:09 2021

@author: 218019067
"""

import os
import numpy as np
from Trial import Trial

class Episode:
    # all trials for one extension state
    def __init__(self, extension_root):
        # 
        self.extension_root_dir = extension_root # "./Data/USV/Extension_0/"
        self.PWM = []
        self.files = []
        
    # end
    
    def expFiles(self, path): # find all trial files
        dirs = os.listdir(path)
        #print(dirs)
        
        self.PWM = []
        self.files = []
        for exp_folder in dirs: # file name with PWM commands
            # get the PWM commands
            folder_name = exp_folder.split('_')
            PWM = [int(folder_name[1]), int(folder_name[3]), int(folder_name[5]), int(folder_name[7])]
        
            # find all experiment files in the path
            exp_files = os.listdir(path+exp_folder+"/")
            for file in exp_files:
                self.files.append(path+exp_folder+"/"+file)
                self.PWM.append(PWM)
        # save self.files and self.PWM
        #print(self.files)
    
    def findAllTrials(self): # find all trials for one extension state
        # 3rd class
        exp_type_dirs = os.listdir(self.extension_root_dir)
        #print(exp_type_dirs)
        for exp_type_dir in exp_type_dirs:
            exp_type_path = self.extension_root_dir + exp_type_dir + "/"
            if os.path.isdir(exp_type_path):
                # 4th class
                exp_dirs = os.listdir(exp_type_path)
                #print(exp_dirs)
                for exp_dir in exp_dirs:
                    self.expFiles(exp_type_path + exp_dir + "/")
        #print(self.files)
        #print()
        
    def setParameters(self, parameters): # parameters is a list with 6 elements
        self.parameters = parameters
        
    def run(self):
        self.findAllTrials()
        error = np.array([])
        for file in self.files:
            #
            sim = Trial(file)
            sim.setParameters(self.parameters)
            sim.trial()
            error = np.append(error, sim.error)
        self.error = error.sum()
        #print("Model error:  ", self.error)
    
# Test script
if __name__ == "__main__":
    # directories
    root_dir = "./Data/USV/"
    ext_dir = ["Extension_0/", "Extension_10/", "Extension_20/", "Extension_30/", "Extension_40/", "Extension_50/"]
    exp_type_dir = ["Circle/", "Spinning/", "StraightLine/"]
    c_set_dir = ["Anticlockwise/", "Clockwise/"]
    l_set_dir = ["Backward/", "Forward/", "Leftward/", "Rightward/"]
    exp_name = "PWM1_0_PWM2_110_PWM3_0_PWM4_110/"
    file_name = "Take 2021-06-13 06.40.43 PM_013.csv"
    
    episode = Episode(root_dir + ext_dir[0])
    episode.setParameters([40, 40, 12, 2, 2, 2])
    episode.run()
    
    
    