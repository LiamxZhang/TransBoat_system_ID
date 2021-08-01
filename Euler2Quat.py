import numpy as np
import math

def euler_to_quaternion(yaw, pitch, roll):

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    # return [qx, qy, qz, qw]
    return [qw, qy, qz, qx]

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

# straight line
# q = euler_to_quaternion(-0.889816407175509 + np.pi, 0.008668946937078526, -0.013423812934876515)
# q = euler_to_quaternion(-0.8918240980449207 + np.pi, 0.006735854654123119, -0.01324196108435154)
# q = euler_to_quaternion(-0.8934454355693141 + np.pi, 0.012686634989740543, -0.01683066426404125)

# Circle
q_lst = []
r_lst = [-0.009583315101425625, -0.009247231449446554, -0.008655977262291059, -0.012573939644392847, -0.01156760905517527, -0.01845162243107244]
p_lst = [0.020778274007532606, -0.009247231449446554, 0.020954913224025176, 0.022975518719573866, 0.022961589917634296, 0.026890234087598705]
y_lst = [-2.065581966866609, -2.0678981053631, -2.069448284738034, -2.0795867457682453, -2.0809196534648273, -2.0846797504679806]
row_lst = list(range(441, 447))

for i in range(6):
    q = euler_to_quaternion(y_lst[i] + np.pi, p_lst[i], r_lst[i])
    print("q: ", q)
    w = QuaternionToEuler(q)
    print("w: ", w)
    print("---------------------------------------------")
    q_lst.append(q)

# w = QuaternionToEuler([q[1], q[2], q[3], q[0]])
