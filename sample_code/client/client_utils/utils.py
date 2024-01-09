import socket
import pickle
import numpy as np
import time
import threading
import cv2
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

TASKBEGIN = b'0'
TASKEND = b'4'
SENDREQUIRE = b'1'
CATCHIMAGE = b'2'
DETECT = b'3'
IMAGEBEGIN = b'8'
IMAGEEND = b'9'

imghigh = 640
imgwidth = 480
actions = [b'a', b'b', b'c', b'd', b'e', b'f', b'g'] 


def defect(image, model):
    image = image[..., ::-1]
    results = model(image, size=(imghigh, imgwidth))  # batch of images
    # 保存图片到客户端
    results.save()
    # 展示图片
    # results.show()
    xyxys = results.xyxy[0]

    maxsquare = 0
    max_box = -1
    pred_nums = xyxys.shape[0]
    if pred_nums == 0:
        return [320.0, 240.0], 6
    else:
        for i in range(pred_nums):
            xyxy = xyxys[i]
            x_dis = xyxy[2] - xyxy[0]
            y_dis = xyxy[3] - xyxy[1]
            square = x_dis * y_dis
            if maxsquare < square:
                maxsquare = square
                max_box = i
        if max_box != -1:
            x = (xyxys[max_box][2] - xyxys[max_box][0])
            y = (xyxys[max_box][3] - xyxys[max_box][1])
        x = float(x.cpu().numpy())
        y = float(y.cpu().numpy())
    classes=int(xyxy[5])
    
    return [x, y], classes


def revice_img(socket):
    tempdata_len = socket.recv(6)
    tempdata_len = tempdata_len.decode()
    data = b''
    count = int(tempdata_len)
    while count:
        recvData = socket.recv(count)
        if not recvData:
            return None
        data += recvData
        count -= len(recvData)

    image_data = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    # cv2.imwrite('F:\\PyFiles\\keshe\\client_utils\\data\\1_p50.png', image)
    return image


def send_server_request(self, client_socket, task, model):
    if task == "task1":
        client_task1(self, client_socket, model)


def client_task1(self, socket, model):
    
    flags = TASKBEGIN  # 1.客户端发送一个任务请求 2.服务器接收到任务请求后，调用摄像头，将摄像头采集到的图像发回给客户端 3.客户端接到图像后进行yolov5检测，检测完的坐标信息发回给服务器
    # 4.服务器处理坐标，调用机器臂进行移动，并告知客户端已完成移动
    while flags != TASKEND:
        if flags == TASKBEGIN: 
            flags = SENDREQUIRE 
            # 发送SENDREQUIRE标志            
            self.log_emitter.log_message("发送 SENDREQUIRE 标志")
            socket.send(flags)
        # 收到CATCHIMAGE标志，检测图片并执行发送动作命令
        elif flags == CATCHIMAGE:
            locate, classes = defect(img, model)            
            self.log_emitter.log_message("发送 classes " + str(classes))
            flags = DETECT
            self.lab_vid.setPixmap(QPixmap("D:\\courseDesignIV\\sample_code - 1.8\\sample_code\\client\\runs\detect\\exp\\image0.jpg"))

            self.log_emitter.log_message("发送 DETECT 标志")
            socket.send(flags)
            socket.send(actions[classes])
        # 收到IMAGEBEGIN标志，等待接受图片（接受并解码图片）
        elif flags == IMAGEBEGIN:
            img = revice_img(socket)
        else:
            self.log_emitter.log_message("服务器处理失败")
            pass

        # 接受一个字节数据(标志)    
        data = socket.recv(1)
        flags = data

        

