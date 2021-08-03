# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 22:53:09 2021

@author: 218019067
"""

import os
import time
import numpy as np
from matplotlib import pyplot as plt
from Trial import Trial

class Episode:
    # all trials for one extension state
    def __init__(self, extension_root):
        # 
        self.extension_root_dir = extension_root # "./Data/USV/Extension_0/"
        # Initialize trials (read experiment data)
        self.findAllTrials()
        self.all_sim = []
        for file in self.files:
            sim = Trial(file)
            self.all_sim.append(sim)
        # self.PWM = []
        # self.files = []
        
    # end
    
    def expFiles(self, path): # find all trial files
        dirs = os.listdir(path)
        #print(dirs)
        
        # self.PWM = []
        # self.files = []
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
        self.PWM = []
        self.files = []
        exp_type_dirs = os.listdir(self.extension_root_dir)
        # print("exp_type_dirs: ", exp_type_dirs)
        for exp_type_dir in exp_type_dirs:
            exp_type_path = self.extension_root_dir + exp_type_dir + "/"
            if os.path.isdir(exp_type_path):
                # 4th class
                exp_dirs = os.listdir(exp_type_path)
                # print("exp_dirs", exp_dirs)
                for exp_dir in exp_dirs:
                    self.expFiles(exp_type_path + exp_dir + "/")
        # print("self.files: ", self.files)
        # print(len(self.files))
        #print()
        
    def setParameters(self, parameters): # parameters is a list with 6 elements
        self.parameters = parameters
        
    def run(self):
        # if not self.readFiles:
        #     self.findAllTrials()
        #     self.all_sim = []
        #     for file in self.files:
        #         sim = Trial(file)
        #         self.all_sim.append(sim)
        #     self.readFiles = True
        self.error_lst = np.array([])
        for sim in self.all_sim:
            print(sim.path)
            # sim = Trial(file)
            sim.setParameters(self.parameters)
            if "Spinning" in sim.path:
                sim.trial([1, 1, 0.5])
                sim.showAngle()
            else:
                sim.trial([1, 1, 1])
                sim.showFigures()
            # plt.figure(file)
            # plt.plot(sim.w_lst)
            # sim.trial([1, 1, 1])
            self.error_lst = np.append(self.error_lst, sim.error)
        self.error = self.error_lst.sum()
        #print("Model error:  ", self.error)

    def showFigures(self):
        plt.figure("episode")
        L = len(self.error_lst)
        # print(L)
        print(self.error_lst)
        x = list(range(1, L+1))
        plt.bar(x, self.error_lst)
        plt.ylabel("Error")
        # plt.title("Equal weight: [1, 1, 1]")
        plt.show()
    
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
    
    # episode.setParameters([40, 40, 12, 2, 2, 2])
    # episode.setParameters([30, 60, 150, 50, 40, 60])
    # err_lst = []
    # x_lst = []
    # episode = Episode(root_dir + ext_dir[0])
    # for i in range(20):
    #     x = 500 + 50 * i
    #     # y = -155000 - 100 * i
    #     x_lst.append(x)
    #     episode.setParameters([41.9, 41.9, 860, 27.49, 27.49, 180])
    #     t1 = time.time()
    #     episode.run()
    #     t2 = time.time()
    #     err_lst.append(episode.error)
    #     print("error", episode.error)
    #     print("x: ", x)
    #     # print("y: ", y)
    #     print("used time: ", t2-t1)
    # plt.plot(x_lst, err_lst)
    # plt.xlabel("x")
    # plt.ylabel("Error")
    # plt.title("m1 = 41.9, m2 = 41.9, m3 = x, d1 = 27.49, d2 = 27.49, d3 = 180")
    # plt.show()

    episode = Episode(root_dir + ext_dir[5])
    episode.setParameters([41.9, 41.9, 860, 27.49, 27.49, 180])
    # episode.setParameters([41.9, 41.9, 385000, 27.49, 27.49, -28000])
    
    # episode.setParameters([41.90259446, 60., 199.98714965, 27.49310886, 600., 445.24579278])
    # episode.setParameters([41.90259446, 30., 10., 27.49310886, 200., 100.])
    # episode.setParameters([41.9, 41.9, 1960000, 27.49, 27.49, -156500])
    t1 = time.time()
    episode.run()
    t2 = time.time()
    print("error", episode.error)
    print("used time: ", t2-t1)
    episode.showFigures()

