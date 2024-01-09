import cv2
import socket
import pickle
import numpy as np
import time
import threading
import Arm_Lib
 

SNEDLENGTH = 1
TASKBEGIN = b'0'
TASKEND = b'4'
SENDREQUIRE = b'1'
CATCHIMAGE = b'2'
DETECT = b'3'
IMAGEBEGIN = b'8'
IMAGEEND = b'9'

# 动作1
from Arm_Lib import Arm_Device

def ctrl_all_servo(angle, s_time = 500):
    Arm.Arm_serial_servo_write6(angle, 180-angle, angle, angle, angle, angle, s_time)
    time.sleep(s_time/1000)

def action1():
    Arm = Arm_Device()
    time.sleep(.1)
    time_1 = 500
    time_2 = 1000
    time_sleep = 0.5
    for i in range(3):
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

# 动作2        
def action2():
    pass
def action3():
    pass
def action4():
    pass
def action5():
    pass

def Action(classes):
    #print('action'+ classes)
    if classes==b'a':
        action1()
    elif classes==1:
        pass
    elif classes==2:
        pass
    elif classes==3:
        pass
    else:
        pass


def camera_read_single_image(server_socket,capture):
    _ ,img = capture.read()
    img = cv2.resize(img,(640,480))
    #img = cv2.imread('C:\\Users\\Lyx\\Desktop\\python\\keshe\\keshe\\server_utils\\data\\1_p50.png')
    img_encode = cv2.imencode('.png', img)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tostring()
    imgsize = len(str_encode)
    has_sent = 0
    server_socket.send(IMAGEBEGIN)
    
    encode_len = str(imgsize).encode()
    
    server_socket.send(encode_len)
    server_socket.send(str_encode)

    #while has_sent <= imgsize:
    #    data_to_send = str_encode[has_sent: has_sent + SNEDLENGTH]
    #    server_socket.send(data_to_send)
    #    has_sent += SNEDLENGTH
    print("read images return a np list")


def send_singel_image():
    return "send an image to client"


def handle_yolo_data():
    print("yolo data")


def worker(server_socket,follow):
    print("worker begin")
    loca_message = server_socket.recv(34)
    x,y = pickle.loads(loca_message)
    follow.follow_function(x,y)
    print("worker end")


def handle_client_request(server_socket, ip_port,capture,follow):
    # 循环接收客户端发送的数据
    while True:
        # 接收客户端发送的数据
        recv_data = server_socket.recv(1)
        if recv_data:
            # data = pickle.loads(recv_data)
            flags = recv_data
            # message = []
            if flags == SENDREQUIRE:
               # send_image_thread = threading.Thread(target=camera_read_single_image,args=(server_socket,capture))
               # send_image_thread.start()
               # time.sleep(0.5)
                camera_read_single_image(server_socket,capture)
                time.sleep(0.01)
                flags = CATCHIMAGE 
                server_socket.send(flags)
                time.sleep(0.25)
            elif flags == DETECT:
                worker(server_socket,follow)
                time.sleep(0.01)

                classes = server_socket.recv(4)
                Action(classes)

                flags = TASKEND
                server_socket.send(flags)
                time.sleep(0.25)
                  
            else:
                print("上一步处理失败")
                server_socket.close()
        else:
            print("客户端下线了:", ip_port)
            break
    # 终止和客户端进行通信
    server_socket.close()
