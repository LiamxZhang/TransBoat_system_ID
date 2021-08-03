# File: Euler2Quat.py
# Run this script to modify the erroneous points of the orientation in the experiment data.
# Modify value of the lower or upper threshold (valL/valU) and delta_w
# as the instruction in __main__ before run this program.

import numpy as np
import math
import csv

from Trial import Trial

def euler_to_quaternion(yaw, pitch, roll):

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    # return [qx, qy, qz, qw]
    # return [qw, qy, qz, qx]
    return [-qy, -qz, -qx, -qw]

def QuaternionToEuler(intput_data, angle_is_rad = True):
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
    if y < -1.5:
        # print("y: ", y, "\t quat: ", w0, y0, z0, x0)
        print("r: ", r, "\t p: ", p, "\t y: ", y)
    return [r,p,y]

def editCSV(path, delta_w, valU = 10, valL = -10):
    trial = Trial(path, valU, valL)
    # Compute the correct Quat
    L = len(trial.rowToBeEdited)
    q_lst = []
    for i in range(L):
        e = trial.EulerToBeEdited[i]
        q = euler_to_quaternion(e[0] + delta_w, e[1], e[2])
        print("Row: ", trial.rowToBeEdited[i], " \t Edited q: ", q)
        w = QuaternionToEuler(q)
        print("w: ", w)
        print("---------------------------------------------")
        q_lst.append(q)
    
    # Edit csv
    rows = []
    with open(path, "r", newline='') as csv_r:
        f_reader = csv.reader(csv_r)
        r_i = 0
        q_i = 0
        for row in f_reader:
            r_i += 1
            if r_i in trial.rowToBeEdited:
                row[2] = q_lst[q_i][0]
                row[3] = q_lst[q_i][1]
                row[4] = q_lst[q_i][2]
                row[5] = q_lst[q_i][3]
                q_i += 1
            rows.append(row)
        # print(rows)

    with open(path, "w", newline='') as csv_w:
        f_writer = csv.writer(csv_w)
        f_writer.writerows(rows)
    
    print("Finish edition of file: ", path)


if __name__ == "__main__":
    # path of the csv file to be edited
    file_name = "./Data/USV/Extension_50/Circle/Clockwise/PWM1_0_PWM2_60_PWM3_0_PWM4_55/Take 2021-06-13 06.40.43 PM_045.csv"

    #path = "./Data/USV/Extension_30/StraightLine/Rightward/PWM1_70_PWM2_0_PWM3_70_PWM4_0/Take 2021-07-09 18.50.59 AM_016.csv"
    #path = "./Data/USV/Extension_20/StraightLine/Forward/PWM1_0_PWM2_50_PWM3_0_PWM4_50/Take 2021-07-09 18.50.59 AM_002.csv"
    delta_w =  np.pi/2     # delta_w = true_w - wrong_w
    # Specify valU to certain threshold if wrong_w > true_w, otherwise specify valL
    editCSV(file_name, delta_w, valL = 0)

# straight line
# q = euler_to_quaternion(-0.889816407175509 + np.pi, 0.008668946937078526, -0.013423812934876515)
# q = euler_to_quaternion(-0.8918240980449207 + np.pi, 0.006735854654123119, -0.01324196108435154)
# q = euler_to_quaternion(1.309447440922361 + np.pi/10, 0.8111379887644137, 2.0895401206273396)
#print(q)

# Circle
# q_lst = []
# r_lst = [-0.009583315101425625, -0.009247231449446554, -0.008655977262291059, -0.012573939644392847, -0.01156760905517527, -0.01845162243107244]
# p_lst = [0.020778274007532606, -0.009247231449446554, 0.020954913224025176, 0.022975518719573866, 0.022961589917634296, 0.026890234087598705]
# y_lst = [-2.065581966866609, -2.0678981053631, -2.069448284738034, -2.0795867457682453, -2.0809196534648273, -2.0846797504679806]
# row_lst = list(range(441, 447))

# for i in range(6):
#     q = euler_to_quaternion(y_lst[i] + np.pi, p_lst[i], r_lst[i])
#     print("q: ", q)
#     w = QuaternionToEuler(q)
#     print("w: ", w)
#     print("---------------------------------------------")
    # q_lst.append(q)

# w = QuaternionToEuler([q[1], q[2], q[3], q[0]])


## Test for editing csv files
# lines = [2, 4]
# rows = []
# rows = [['1', '2', '7'], ['2', '3', 0.1], ['3', '3', '8'], ['4', '4', 0.1], ['5', '5', '3'], ['6', '6', '1']]
# with open("testCSV.csv", "w", newline='') as csv_f:
#     f_reader = csv.reader(csv_f)
#     r_i = 0
#     for row in f_reader:
#         r_i += 1
#         if r_i in lines:
#             row[2] = 0.1
#         rows.append(row)
#     print(rows)
#     f_writer = csv.writer(csv_f)
#     f_writer.writerows(rows)
