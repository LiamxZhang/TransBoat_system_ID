# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 22:46:37 2021

@author: 218019067
"""

import csv
import math
import numpy as np
from matplotlib import pyplot as plt
from USVmodel import USVmodel


class Trial: 
    # one single trial of experiment
    def __init__(self, path, valU = 10, valL = -10):
        self.path = path
        # get the extension information
        self.extension = int(path.split("/")[3].split("_")[1])
        #print(self.extension)
        # get the pwm command
        self.PWM = [int(i) for i in path.split("/")[6].split("_")[1::2]]
        #print(self.PWM)
        # get all data
        t_e = 10   # time: s
        self.readCSV(path, t_e, valU, valL)
    
    def readCSV(self, file_path, end_t = 10, valU = 10, valL = -10):
        # read csv files to obtain the initial state and the time list
        header = 7 # jump the header
        deque_length = 10 # jump the first data
        skip_sec = 1 # skip the first 1 second
        # get_initial_state_flag = False # whether the initial state obtained
        #
        self.t_lst = []
        
        self.x_lst = []
        self.y_lst = []
        self.w_lst = []
        
        self.velx_lst = []
        self.vely_lst = []
        self.velw_lst = []
        
        self.state_deque = []

        self.rowToBeEdited = []     # Row index
        self.EulerToBeEdited = []   # List of y, p, r to be edited
        
        with open(file_path, newline='') as csv_f:
            f_reader = csv.reader(csv_f)
            row_i = 0 # count which row
            data_i = 0 # count which data
            for row in f_reader:
                row_i += 1
                
                # skip the headers
                if row_i <= header:
                    continue
                
                # skip the empty row
                if row[2] == '':
                    continue
                
                data_i += 1 # all next are data
                
                # prepare data
                t = eval(row[1])

                if t > end_t:
                    # print("t = 10 s")
                    self.t = end_t
                    break

                x, y, w, r0, p0, y0 = self.getXYW(row)
                
                # skip the first 10 data
                if data_i <= deque_length:
                    self.state_deque.append([t, x, y, w])
                    continue
                
                # calculate the speed for every 10 data
                self.state_deque.append([t, x, y, w])
                #print(self.state_deque)
                delta_t = self.state_deque[-1][0] - self.state_deque[0][0]
                vel_x = (self.state_deque[-1][1] - self.state_deque[0][1])/delta_t
                vel_y = (self.state_deque[-1][2] - self.state_deque[0][2])/delta_t
                diff = self.state_deque[-1][3] - self.state_deque[0][3]
                if diff > np.pi:
                    diff = -(2 * np.pi - diff)
                elif diff < -np.pi:
                    diff = -(-2 * np.pi - diff)
                vel_w = diff/delta_t
                # print("1: ", self.state_deque[-1][3], "\t 2: ", self.state_deque[0][3], "\t delta_t: ", delta_t, "\t vel_w: ", vel_w)
                self.state_deque.pop(0)
                
            #    if not get_initial_state_flag:
            #        # calculate the speed for every 10 data
            #        if data_i == 1:
            #            init_x, init_y, init_w = x, y, w
            #            t_last = t
            #        elif data_i % 10 == 1:
            #            delta_t = t - t_last
            #            vel_x = (x-init_x)/delta_t
            #            vel_y = (y-init_y)/delta_t
            #            vel_w = (w-init_w)/delta_t
            #            init_x = x
            #            init_y = y
            #            init_w = w
            #            t_last = t
                    
                # skip the first second
                if t <= skip_sec: 
                    continue
                
                # to be edit
                if w < valL or w > valU:
                    self.rowToBeEdited.append(row_i)
                    print("w: ", w, "\t row i: ", row_i, "\t t: ", t)
                    self.EulerToBeEdited.append([y0, p0, r0])
                    print("r: ", r0, "\t p: ", p0, "\t y: ", y0)
                    
                t, x, y, w = self.state_deque[int(deque_length/2)]
                # for after the first second
                self.t_lst.append(t)
                self.x_lst.append(x)
                self.y_lst.append(y)
                self.w_lst.append(w)
                self.velx_lst.append(vel_x)
                self.vely_lst.append(vel_y)
                self.velw_lst.append(vel_w)
                
            #    if not get_initial_state_flag:
            #        get_initial_state_flag = True
            #        self.initial_state.append(x)
            #        self.initial_state.append(y)
            #        self.initial_state.append(w)
            #        self.initial_state.append(vel_x)
            #        self.initial_state.append(vel_y)
            #        self.initial_state.append(vel_w)           
        # x, y, w, velx, vely, velw
        self.initial_state = [self.x_lst[0], self.y_lst[0], self.w_lst[0],
                              self.velx_lst[0], self.vely_lst[0], self.velw_lst[0]] 
        self.t = self.t_lst[-1]
        
        #print(self.t_lst)
        #print(self.initial_state)
    
    def QuaternionToEuler(self, intput_data, angle_is_rad = True):
        # change angle vale to radian if False
    
        w0 = intput_data[0] 
        y0 = intput_data[1]    # x
        z0 = intput_data[2]    # y
        x0 = intput_data[3]    # z
    
        r = math.atan2(2 * (w0 * x0 + y0 * z0), 1 - 2 * (x0 * x0 + y0 * y0))
        p = math.asin(2 * (w0 * y0 - z0 * x0))
        y = math.atan2(2 * (w0 * z0 + x0 * y0), 1 - 2 * (y0 * y0 + z0 * z0))
    
        if not angle_is_rad: # pi -> 180
    
            r = r / math.pi * 180
            p = p / math.pi * 180
            y = y / math.pi * 180

        # print("y: ", y)
#        if y < 1.32:
#            print("y: ", y, "\t quat: ", w0, y0, z0, x0)
#            print("r: ", r, "\t p: ", p, "\t y: ", y)
        return [r,p,y]
    
    def getXYW(self, row):
        qx1, qy1, qz1, qw1 = eval(row[2]), eval(row[3]), eval(row[4]), eval(row[5])
        q1 = [qw1, qx1, qy1, qz1]
        w =  self.QuaternionToEuler(q1)[2]
        x = eval(row[8])
        y = eval(row[6])
        r0, p0, y0 = self.QuaternionToEuler(q1)
        return x, y, w, r0, p0, y0
    
    def InertvToBodyv(self, inertial_v, w):
        # inertial_v is a list
        R = np.array([[math.cos(w), -math.sin(w), 0],
                    [math.sin(w), math.cos(w), 0],
                    [0, 0, 1]])
        inertial_v = np.transpose(np.array(inertial_v))
        body_v = np.matmul(np.linalg.inv(R), inertial_v)
        return body_v.tolist() # return a list
    
    def setParameters(self, parameters):
        # m1, m2, m3, d1, d2, d3
        self.mass = parameters[0:3]
        self.drag = parameters[3:6]
        
    def setErrorWeight(self, w):
        self.errorWeight = np.diag(np.array(w))
    
    def errorCalculation(self, Ve, Vs, W):
        # Ve is the 2D experimental velocity
        # Vs is the 2D simulation velocity
        # W is the weight
        if len(Ve) == len(Vs):
            error = np.array([])
            i = 0
            for ve, vs in zip(Ve, Vs):
                e = np.array([i - j for i,j in zip(ve,vs)])
                # if e[2] > 10:
                # print("e: ", e, "\t i: ", i)
                error = np.append(error, np.dot(np.dot(e, W), e.T))
                i += 1

            # print("error: ", error)
            
            return error.sum()
        else:
            print("Wrong velocity dimension!")
            return 0
    
    def trial(self, w = [1,1,0.01]): 
        # new a USVmodel
        # init_vel = self.InertvToBodyv(self.initial_state[3:6], self.initial_state[2])
        USV = USVmodel(self.initial_state[0:3], self.initial_state[3:6], self.extension)    
        
        # set parameter
        USV.setMass(self.mass)
        USV.setDrag(self.drag)
        USV.pwmToPropulsion(self.PWM)

        # simulation
        last_t = self.t_lst[0]
        for t in self.t_lst[1:]:
            delta_t = t - last_t
            USV.update(delta_t)
            last_t = t
        
        # prepare data
        Vel_exp = [[i,j,k] for i,j,k in zip(self.velx_lst, self.vely_lst, self.velw_lst)]
        Vel_sim = USV.state_history[:, 3:6].tolist()
        # print("vel_sim: ", Vel_sim)
        # l = len(Vel_exp)
        # for idx in range(l):
        #     print("exp: ", Vel_exp[idx][2])
        #     print("sim: ", Vel_sim[idx][2])
        self.x_sim_lst = USV.state_history[:, 0].tolist()
        self.y_sim_lst = USV.state_history[:, 1].tolist()
        self.w_sim_lst = USV.state_history[:, 2].tolist()
        self.setErrorWeight(w)
        self.error = self.errorCalculation(Vel_exp, Vel_sim, self.errorWeight)
        #print(self.error)
        #
        #print(USV.state_history)
    
    def drawArrow(self, x, y, w, scale, color):
        # scale = 0.01
        dx = np.cos(w) * scale
        dy = np.sin(w) * scale
        plt.arrow(x, y, dx, dy, 
                width=0.01*scale, head_width=0.2*scale, head_length=0.1*scale, 
                shape="full",
                fc=color, ec=color)
    
    def showFigures(self):
        plt.figure(self.path)
        plt.text(self.initial_state[0], self.initial_state[1], "Origin")
        # draw Arrow
        arrow_scale = 0.01
        x_span = np.max(self.x_lst) - np.min(self.x_lst)
        y_span = np.max(self.y_lst) - np.min(self.y_lst)
        arrow_scale *= np.min([x_span, y_span])
        
        L = len(self.t_lst)
        for i in range(L):
            self.drawArrow(self.x_lst[i], self.y_lst[i], self.w_lst[i], arrow_scale, "b")
            self.drawArrow(self.x_sim_lst[i], self.y_sim_lst[i], self.w_sim_lst[i],
                            arrow_scale, "r")
            
        plt.plot(self.x_lst, self.y_lst, label="Experiment")
        plt.plot(self.x_sim_lst, self.y_sim_lst, label="Simulation")
        plt.legend()
        # plt.show()

    def showAngle(self):
        plt.figure(self.path)
        plt.plot(self.w_lst, label="Exp")
        plt.plot(self.w_sim_lst, label="Sim")
        plt.legend()
        
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
    
    # entity the simulation
    # trial = Trial(root_dir + ext_dir[0] + exp_type_dir[2] + l_set_dir[0] + exp_name + file_name)
    
    # file_name = "./Data/USV/Extension_0/Spinning/Clockwise/PWM1_120_PWM2_120_PWM3_60_PWM4_60/Take 2021-06-13 06.40.43 PM_023.csv"
    # file_name = "./Data/USV/Extension_0/Spinning/Anticlockwise/PWM1_60_PWM2_60_PWM3_120_PWM4_120/Take 2021-06-13 06.40.43 PM_021.csv"
    # file_name = "./Data/USV/Extension_0/Spinning/Anticlockwise/PWM1_70_PWM2_70_PWM3_110_PWM4_110/Take 2021-06-13 06.40.43 PM_022.csv"
    # file_name = "./Data/USV/Extension_0/Spinning/Clockwise/PWM1_110_PWM2_110_PWM3_70_PWM4_70/Take 2021-06-13 06.40.43 PM_024.csv"
    # file_name = "./Data/USV/Extension_0/Circle/Clockwise/PWM1_0_PWM2_65_PWM3_0_PWM4_60/Take 2021-06-13 06.40.43 PM_019.csv"
    # file_name = "./Data/USV/Extension_0/Circle/Anticlockwise/PWM1_0_PWM2_60_PWM3_0_PWM4_65/Take 2021-06-13 06.40.43 PM_017.csv"
    # file_name = "./Data/USV/Extension_0/Circle/Clockwise/PWM1_0_PWM2_65_PWM3_0_PWM4_60/Take 2021-06-13 06.40.43 PM_019.csv"
    # file_name = "./Data/USV/Extension_0/StraightLine/Backward/PWM1_0_PWM2_130_PWM3_0_PWM4_130/Take 2021-06-13 06.40.43 PM_015.csv"
    # file_name = "./Data/USV/Extension_0/StraightLine/Rightward/PWM1_70_PWM2_0_PWM3_70_PWM4_0/Take 2021-06-13 06.40.43 PM_012.csv"
    
    # file_name = "./Data/USV/Extension_10/StraightLine/Forward/PWM1_0_PWM2_70_PWM3_0_PWM4_70/Take 2021-07-09 18.50.59 AM_004.csv"
    # file_name = "./Data/USV/Extension_10/StraightLine/Rightward/PWM1_40_PWM2_0_PWM3_40_PWM4_0/Take 2021-07-09 18.50.59 AM_013.csv"
    # file_name = "./Data/USV/Extension_20/Spinning/Clockwise/PWM1_110_PWM2_110_PWM3_70_PWM4_70/Take 2021-07-09 18.50.59 AM_025.csv"
    # file_name = "./Data/USV/Extension_20/StraightLine/Rightward/PWM1_50_PWM2_0_PWM3_50_PWM4_0/Take 2021-07-09 18.50.59 AM_014.csv"
    # file_name = "./Data/USV/Extension_20/StraightLine/Forward/PWM1_0_PWM2_50_PWM3_0_PWM4_50/Take 2021-07-09 18.50.59 AM_002.csv"
    # file_name = "./Data/USV/Extension_20/StraightLine/Rightward/PWM1_40_PWM2_0_PWM3_40_PWM4_0/Take 2021-07-09 18.50.59 AM_013.csv"
    
    # file_name = "./Data/USV/Extension_30/StraightLine/Rightward/PWM1_70_PWM2_0_PWM3_70_PWM4_0/Take 2021-07-09 18.50.59 AM_016.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Rightward/PWM1_60_PWM2_0_PWM3_60_PWM4_0/Take 2021-07-09 18.50.59 AM_015.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Rightward/PWM1_50_PWM2_0_PWM3_50_PWM4_0/Take 2021-07-09 18.50.59 AM_014.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Forward/PWM1_0_PWM2_50_PWM3_0_PWM4_50/Take 2021-07-09 18.50.59 AM_002.csv"
    # file_name = "./Data/USV/Extension_30/Spinning/Clockwise/PWM1_120_PWM2_120_PWM3_60_PWM4_60/Take 2021-07-09 18.50.59 AM_026.csv"
    # file_name = "./Data/USV/Extension_30/Spinning/Anticlockwise/PWM1_60_PWM2_60_PWM3_120_PWM4_120/Take 2021-07-09 18.50.59 AM_023.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Rightward/PWM1_40_PWM2_0_PWM3_40_PWM4_0/Take 2021-07-09 18.50.59 AM_013.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Forward/PWM1_0_PWM2_40_PWM3_0_PWM4_40/Take 2021-07-09 18.50.59 AM_001.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Backward/PWM1_0_PWM2_130_PWM3_0_PWM4_130/Take 2021-07-09 18.50.59 AM_007.csv"
    # file_name = "./Data/USV/Extension_30/StraightLine/Backward/PWM1_0_PWM2_120_PWM3_0_PWM4_120/Take 2021-07-09 18.50.59 AM_006.csv"

    # file_name = "./Data/USV/Extension_40/Spinning/Anticlockwise/PWM1_60_PWM2_60_PWM3_120_PWM4_120/Take 2021-07-09 18.50.59 AM_024.csv"
    # file_name = "./Data/USV/Extension_40/Spinning/Anticlockwise/PWM1_70_PWM2_70_PWM3_110_PWM4_110/Take 2021-07-09 18.50.59 AM_025.csv"
    # file_name = "./Data/USV/Extension_40/Spinning/Clockwise/PWM1_120_PWM2_120_PWM3_60_PWM4_60/Take 2021-07-09 18.50.59 AM_027.csv"
    # file_name = "./Data/USV/Extension_40/Circle/Anticlockwise/PWM1_0_PWM2_54_PWM3_0_PWM4_60/Take 2021-07-09 18.50.59 AM_020.csv"
    # file_name = "./Data/USV/Extension_40/Circle/Anticlockwise/PWM1_0_PWM2_59_PWM3_0_PWM4_65/Take 2021-07-09 18.50.59 AM_017.csv"
    # file_name = "./Data/USV/Extension_40/Circle/Anticlockwise/PWM1_0_PWM2_64_PWM3_0_PWM4_70/Take 2021-07-09 18.50.59 AM_019.csv"
    # file_name = "./Data/USV/Extension_40/Circle/Clockwise/PWM1_0_PWM2_60_PWM3_0_PWM4_55/Take 2021-07-09 18.50.59 AM_021.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Rightward/PWM1_70_PWM2_0_PWM3_70_PWM4_0/Take 2021-07-09 18.50.59 AM_016.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Leftward/PWM1_120_PWM2_0_PWM3_120_PWM4_0/Take 2021-07-09 18.50.59 AM_010.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Forward/PWM1_0_PWM2_60_PWM3_0_PWM4_60/Take 2021-07-09 18.50.59 AM_002.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Backward/PWM1_0_PWM2_130_PWM3_0_PWM4_130/Take 2021-07-09 18.50.59 AM_006.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Backward/PWM1_0_PWM2_120_PWM3_0_PWM4_120/Take 2021-07-09 18.50.59 AM_005.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Rightward/PWM1_60_PWM2_0_PWM3_60_PWM4_0/Take 2021-07-09 18.50.59 AM_015.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Rightward/PWM1_40_PWM2_0_PWM3_40_PWM4_0/Take 2021-07-09 18.50.59 AM_013.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Leftward/PWM1_140_PWM2_0_PWM3_140_PWM4_0/Take 2021-07-09 18.50.59 AM_012.csv"
    # file_name = "./Data/USV/Extension_40/StraightLine/Leftward/PWM1_130_PWM2_0_PWM3_130_PWM4_0/Take 2021-07-09 18.50.59 AM_011.csv"

    # file_name = "./Data/USV/Extension_50/Circle/Clockwise/PWM1_0_PWM2_60_PWM3_0_PWM4_55/Take 2021-06-13 06.40.43 PM_045.csv"
    # file_name = "./Data/USV/Extension_50/Spinning/Anticlockwise/PWM1_60_PWM2_60_PWM3_120_PWM4_120/Take 2021-06-13 06.40.43 PM_046.csv"
    # file_name = "./Data/USV/Extension_50/Spinning/Anticlockwise/PWM1_70_PWM2_70_PWM3_110_PWM4_110/Take 2021-06-13 06.40.43 PM_047.csv"
    # file_name = "./Data/USV/Extension_50/Spinning/Clockwise/PWM1_110_PWM2_110_PWM3_70_PWM4_70/Take 2021-06-13 06.40.43 PM_049.csv"
    # file_name = "./Data/USV/Extension_50/Spinning/Clockwise/PWM1_120_PWM2_120_PWM3_60_PWM4_60/Take 2021-06-13 06.40.43 PM_048.csv"
    
    trial = Trial(file_name)
    #OASES.setMass(2, 1, 1.2)
    #OASES.setDrag(0.02, 0.01, 0.02)
    
    #
    #sim.expFiles()
    #sim.readCSV(sim.files[0])
    # trial.setParameters([41.9, 41.9, 1960000, 27.49, 27.49, -156500])
    # trial.setParameters([41.9, 41.9, 150, 27.49, 27.49, 60])
    trial.setParameters([41.9, 41.9, 860, 27.49, 27.49, 180])
    # trial.setParameters([37.5683254, 56.24252949, 88.67227952, 3.24811066, 3.23008923, 40])
    trial.trial([1, 1, 1])
    print(trial.error)
    print("t: ", trial.t)
    print(len(trial.t_lst))
    plt.plot(trial.w_lst, label="Exp")
    # plt.plot(trial.w_sim_lst, label="Sim")
    # plt.legend()
    # trial.showAngle()
    # print("exp origin w:")
    # trial.showFigures()
    plt.show()
    