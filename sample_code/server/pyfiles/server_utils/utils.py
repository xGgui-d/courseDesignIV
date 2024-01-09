import cv2
import socket
import pickle
import numpy as np
import time
import threading
import Arm_Lib

from Arm_Lib import Arm_Device
Arm = Arm_Device()
time.sleep(.1)


SNEDLENGTH = 1
TASKBEGIN = b'0'
TASKEND = b'4'
SENDREQUIRE = b'1'
CATCHIMAGE = b'2'
DETECT = b'3'
IMAGEBEGIN = b'8'
IMAGEEND = b'9'


'''
### 动作1.dance ### 
'''
def action1():
    time_1 = 500
    time_2 = 1000
    time_sleep = 0.5
    for i in range(2):
        Arm.Arm_serial_servo_write(2, 180-60, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(3, 60, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 60, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(2, 180-45, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(3, 45, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 45, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(2, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(3, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 90, time_1)
        time.sleep(.001)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(4, 20, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(6, 150, time_1)
        time.sleep(.001)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(4, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(6, 90, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(4, 20, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(6, 150, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(4, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(6, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(1, 0, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(5, 0, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(3, 180, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 0, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(6, 180, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(6, 0, time_2)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(6, 90, time_2)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(1, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(5, 90, time_1)
        time.sleep(time_sleep)

        Arm.Arm_serial_servo_write(3, 90, time_1)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 90, time_1)
        time.sleep(time_sleep)

        # 复原
        joints_0 = [90, 150, 20, 20, 90, 30]
        Arm.Arm_serial_servo_write6_array(joints_0, 1500)


'''
### 动作2.left_right ### 
'''
def action2():
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
    for i in range(2):
        # Control the up and down operation of No. 3 and No. 4 steering gear
        # 控制3号和4号舵机上下运行
        Arm.Arm_serial_servo_write(3, 0, 1000)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 180, 1000)
        time.sleep(1)
        
        # Control the left and right movement of No. 1 steering gear
        # 控制1号舵机左右运动
        Arm.Arm_serial_servo_write(1, 180, 500)
        time.sleep(.5)
        Arm.Arm_serial_servo_write(1, 0, 1000)
        time.sleep(1)
        
        # Control the steering gear to return to the initial position
        # 控制舵机恢复初始位置
        Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
        time.sleep(1.5)

        # 复原
        joints_0 = [90, 150, 20, 20, 90, 30]
        Arm.Arm_serial_servo_write6_array(joints_0, 1500)


'''
### 动作3.head_up ### 
'''
def arm_clamp_block(enable):
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 135, 400)
    time.sleep(.5)

    
def arm_move(p, s_time = 500):
    for i in range(5):
        id = i + 1
        if id == 5:
            time.sleep(.1)
            Arm.Arm_serial_servo_write(id, p[i], int(s_time*1.2))
        elif id == 1 :
            Arm.Arm_serial_servo_write(id, p[i], int(3*s_time/4))

        else:
            Arm.Arm_serial_servo_write(id, p[i], int(s_time))
        time.sleep(.01)
    time.sleep(s_time/1000)
                
def action3():
    p_mould = [90, 130, 0, 0, 90]
    p_top = [90, 80, 50, 50, 270]


    p_layer_4 = [90, 76, 40, 17, 270]
    p_layer_3 = [90, 65, 44, 17, 270]
    p_layer_2 = [90, 65, 25, 36, 270]
    p_layer_1 = [90, 48, 35, 30, 270]

    p_Yellow = [65, 22, 64, 56, 270]
    p_Red = [118, 19, 66, 56, 270]

    p_Green = [136, 66, 20, 29, 270]
    p_Blue = [44, 66, 20, 28, 270]

    # Move the manipulator to a position ready for grasping
    # 让机械臂移动到一个准备抓取的位置
    arm_clamp_block(0)
    arm_move(p_mould, 1000)
    time.sleep(1)

    # Take the squares in the yellow area and stack them to the bottom position in the middle.
    # 夹取黄色区域的方块堆叠到中间最底层的位置。
    arm_move(p_top, 1000)
    arm_move(p_Yellow, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_layer_1, 1000)
    arm_clamp_block(0)

    time.sleep(.1)

    arm_move(p_mould, 1100)
        
    # time.sleep(1)

    # Clip the blocks in the red area and stack them to the middle second layer.
    # 夹取红色区域的方块堆叠到中间第二层的位置。
    arm_move(p_top, 1000)
    arm_move(p_Red, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_layer_2, 1000)
    arm_clamp_block(0)

    time.sleep(.1)

    arm_move(p_mould, 1100)

    # time.sleep(1)
    # 复原
    joints_0 = [90, 150, 20, 20, 90, 30]
    Arm.Arm_serial_servo_write6_array(joints_0, 1500)


'''
### 动作4.beep ### 
'''
def action4():
    # The buzzer will automatically sound and turn off after 100 milliseconds
    # 蜂鸣器自动响100毫秒后关闭
    b_time = 1
    Arm.Arm_Buzzer_On(b_time)
    time.sleep(1)
    # The buzzer will automatically sound and turn off after 300 milliseconds
    # 蜂鸣器自动响300毫秒后关闭
    b_time = 3
    Arm.Arm_Buzzer_On(b_time)
    time.sleep(1)
    # The buzzer will automatically sound and turn off after 300 milliseconds
    # 蜂鸣器自动响300毫秒后关闭
    b_time = 3
    Arm.Arm_Buzzer_On(b_time)
    time.sleep(1)

    # Turn off the buzzer
    # 关闭蜂鸣器
    Arm.Arm_Buzzer_Off()
    time.sleep(1)


'''
### 动作5.clamp_block ### 
'''
# Define the function of sandwich block, enable = 1: clamp, = 0: loosen
# 定义夹积木块函数，enable=1：夹住，=0：松开
def arm_clamp_block(enable):
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 135, 400)
    time.sleep(.5)

    
# Define the function of mobile manipulator and control the motion of No. 1-5 steering gear at the same time, P = [S1, S2, S3, S4, S5]
# 定义移动机械臂函数,同时控制1-5号舵机运动，p=[S1,S2,S3,S4,S5]
def arm_move(p, s_time = 500):
    for i in range(5):
        id = i + 1
        if id == 5:
            time.sleep(.1)
            Arm.Arm_serial_servo_write(id, p[i], int(s_time*1.2))
        else :
            Arm.Arm_serial_servo_write(id, p[i], s_time)
        time.sleep(.01)
    time.sleep(s_time/1000)

# The manipulator moves upward
# 机械臂向上移动
def arm_move_up():
    Arm.Arm_serial_servo_write(2, 90, 1500)
    Arm.Arm_serial_servo_write(3, 90, 1500)
    Arm.Arm_serial_servo_write(4, 90, 1500)
    time.sleep(.1)

def action5():
    # Define variable parameters at different locations
    # 定义不同位置的变量参数
    p_mould = [90, 130, 0, 0, 90]
    p_top = [90, 80, 50, 50, 270]
    p_Brown = [90, 53, 33, 36, 270]

    p_Yellow = [65, 22, 64, 56, 270]
    p_Red = [117, 19, 66, 56, 270]

    # Move the manipulator to a position ready for grasping
    # 让机械臂移动到一个准备抓取的位置
    arm_clamp_block(0)
    arm_move(p_mould, 1000)
    time.sleep(1)

    # Grab a block from the gray block and put it on the yellow block.
    # 从灰色积木块位置抓取一块积木放到黄色积木块的位置上。
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Yellow, 1000)
    arm_clamp_block(0)


    arm_move(p_mould, 1000)

    time.sleep(1)

    # Grab a block from the gray block and put it on the red block.
    # 从灰色积木块位置抓取一块积木放到红色积木块的位置上。
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Red, 1000)
    arm_clamp_block(0)

    arm_move_up()
    arm_move(p_mould, 1100)

    time.sleep(1)    
    # 复原
    joints_0 = [90, 150, 20, 20, 90, 30]
    Arm.Arm_serial_servo_write6_array(joints_0, 1500)
    

'''
### 动作6.rbg ### 
'''
def action6():

    Arm.Arm_RGB_set(50, 0, 0) #RGB亮红灯  RGB red
    time.sleep(.5)
    Arm.Arm_RGB_set(0, 50, 0) #RGB亮绿灯  RGB green
    time.sleep(.5)
    Arm.Arm_RGB_set(0, 0, 50) #RGB亮蓝灯  RGB blue
    time.sleep(.5)

    Arm.Arm_RGB_set(50, 0, 0) #RGB亮红灯  RGB red
    time.sleep(.5)
    Arm.Arm_RGB_set(0, 50, 0) #RGB亮绿灯  RGB green
    time.sleep(.5)
    Arm.Arm_RGB_set(0, 0, 50) #RGB亮蓝灯  RGB blue
    time.sleep(.5)            


# 动作路由
def doAction(classes):
    if classes == b'a':
        print(f'检测到类别{classes}, 正在执行动作 1')
        action1()
    elif classes == b'b':
        print(f'检测到类别{classes}, 正在执行动作 2')
        action2()        
    elif classes == b'c':
        print(f'检测到类别{classes}, 正在执行动作 3')
        action3()           
    elif classes == b'd':
        print(f'检测到类别{classes}, 正在执行动作 4')
        action4()         
    elif classes == b'e':
        print(f'检测到类别{classes}, 正在执行动作 5')
        action5()         
    elif classes == b'f':
        print(f'检测到类别{classes}, 正在执行动作 6')
        action6()              
    else:
        pass


def camera_read_single_image(server_socket,capture):
    _ ,img = capture.read()
    img = cv2.resize(img,(640,480))
    img = cv2.rotate(img, cv2.ROTATE_180)
    img_encode = cv2.imencode('.png', img)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tostring()
    imgsize = len(str_encode)
    has_sent = 0
    # 发送IMAGEBEGIN标志，提示客户端开始接受图片
    server_socket.send(IMAGEBEGIN)
    
    encode_len = str(imgsize).encode()
    
    server_socket.send(encode_len)
    server_socket.send(str_encode)
    print("read images return a np list")


def send_singel_image():
    return "send an image to client"


def handle_yolo_data():
    print("yolo data")


def worker(server_socket, follow):
    print("worker begin")
    loca_message = server_socket.recv(34)
    x, y = pickle.loads(loca_message)
    follow.follow_function(x, y)
    print("worker end")


def handle_client_request(server_socket, ip_port, capture, follow):
    # 循环接收客户端发送的数据
    while True:
        # 接收客户端发送的数据
        recv_data = server_socket.recv(1)
        if recv_data:
            flags = recv_data
            # 如果收到SENDREQUIRE标志，从摄像头读取一帧图片并发送
            if flags == SENDREQUIRE:
                camera_read_single_image(server_socket, capture)
                flags = CATCHIMAGE 
                # 发送CATCHIMAGE标志
                print("发送 CATCHIMAGE 标志")
                server_socket.send(flags)
                # 如果收到DETECT标志，将执行动作
            elif flags == DETECT:
                # worker(server_socket, follow)
                # 接受客户端的classes，根据classes选择并执行动作
                classes = server_socket.recv(4)
                doAction(classes)
                # 发送任务完成标志
                flags = TASKEND
                print('发送 TASKEND 标志')
                server_socket.send(flags)          
            else:
                print("上一步处理失败")
                server_socket.close()
        else:
            print("客户端下线了:", ip_port)
            break
    # 终止和客户端进行通信
    server_socket.close()
