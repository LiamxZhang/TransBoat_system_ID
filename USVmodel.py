# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:30:56 2021

@author: 218019067
"""
import numpy as np
from matplotlib import pyplot as plt
import math
from ThrusterModel import ThrusterModel

# USV model
class USVmodel:
    def __init__(self):
        self.position = np.transpose(np.array([0, 0, 0])) # position and posture
        self.velocity = np.transpose(np.array([0, 0, 0])) # inertial frame
        self.extension = 0
        
    def __init__(self, init_position, init_velocity, init_extension = 0):
        self.position = np.transpose(np.array(init_position)) # x, y, w
        self.velocity = np.transpose(np.array(init_velocity)) # u, v, r (inertial frame)
        self.extension = init_extension
        
        self.main_hull_length = 50 # length of main hull
        
        self.state_history = np.hstack((np.transpose(self.position), np.transpose(self.velocity)))
        
        # transformation matrix
        self.__updateR()
        self.bodyV = np.matmul(np.linalg.inv(self.R), self.velocity) # x_dot, y_dot, w_dot (body frame)
    
    def setMass(self, m):
        if len(m) == 3:
            self.Mass = np.diag(np.array(m))
    
    def setDrag(self, d):
        if len(d) == 3:
            self.Drag = np.diag(np.array(d))
    
    def setPropulsion(self, prop): # 4 thrusters
        e0 = self.main_hull_length/2 # extension base
        e1 = self.extension
        e2 = self.extension
        e3 = self.extension
        e4 = self.extension
        self.B = np.array([[0, 1, 0, 1],
                           [1, 0, 1, 0],
                           [-(e0+e1), -(e0+e2), e0+e3, e0+e4]])
        p_array = np.transpose(np.array(prop))
        self.propulsion = np.matmul(self.B, p_array)
    
    def pwmToPropulsion(self, pwm): # pwm is a list of 4 pwms
        if not 'self.thrusters' in locals().keys(): # if self.thrusters not exist
            self.thrusters = []
            for i in range(4):
                # new thruster
                self.thrusters.append(ThrusterModel(i+1))
                #self.thrusters[i].showFigures()
        # get propulsion        
        prop = []    
        for i in range(4):
                prop.append(self.thrusters[i].propulsion(pwm[i]))
        #        
        self.setPropulsion(prop)
        
    def setExtension(self, extension):
        self.extension = extension
    
    def __updateCoriolis(self):
        m1 = self.Mass[0][0]
        m2 = self.Mass[1][1]
        self.Coriolis = np.array([[0, 0, -m2 * self.bodyV[1]],
                                   [0, 0, m1 * self.bodyV[0]],
                                   [m2 * self.bodyV[1], -m1 * self.bodyV[0], 0]])
    
    def __updateInertialV(self): # bodyV is a column vector of numpy array
        self.__updateR()
        self.velocity = np.matmul(self.R, self.bodyV)

    def __updateR(self):
        # transformation matrix
        w = self.position[2]
        self.R = np.array([[math.cos(w), -math.sin(w), 0],
                            [math.sin(w), math.cos(w), 0],
                            [0, 0, 1]])
    
    # update model
    def update(self, T=0.1): # T is the time interval
        # update velocity
        self.__updateCoriolis()
        M_inv = np.linalg.inv(self.Mass)
        CDv = np.matmul((self.Coriolis+self.Drag), self.bodyV)
        self.bodyV += T * (np.matmul(M_inv, self.propulsion - CDv))
        
        # update position
        self.__updateR()
        self.velocity = np.matmul(self.R, self.bodyV)
        self.position += T * self.velocity
        
        # save to state history
        state = np.hstack((np.transpose(self.position), np.transpose(self.velocity)))
        #print(state)
        self.state_history = np.vstack((self.state_history, state))
        
    # show figures
    def showFigures(self):
        print(self.state_history)
        plt.plot([i[0] for i in self.state_history], [i[1] for i in self.state_history])
        plt.show()
        
# Test script
if __name__ == "__main__":
    state = [0.0, 0.0, 0.0]
    velocity = [0.0, 0.0, 0.0]
    usv1 = USVmodel(state, velocity, 0)
    usv1.setMass([2, 1, 1.2])
    usv1.setDrag([0.02, 0.01, 0.02])
    usv1.setPropulsion([0.02, 0, 0.02, 0])
    x = []
    y = []
    w = []
    
    for i in range(100):
        #print("position: ", usv1.position)
        #print("velocity: ", usv1.velocity)
        x.append(usv1.position[0])
        y.append(usv1.position[1])
        w.append(usv1.position[2])
        usv1.update()

    #plt.plot(x, y)
    #plt.show()
    # print(usv1.state_history)
    usv1.showFigures()
