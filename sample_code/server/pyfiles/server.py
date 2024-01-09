import socket
from server_utils.utils import *
import pickle
import threading
import cv2
from server_utils.object_follow import *

import Arm_Lib
Arm = Arm_Lib.Arm_Device()
joints_0 = [90, 150, 20, 20, 90, 30]
Arm.Arm_serial_servo_write6_array(joints_0, 1500)
follow = object_follow()


def exit_server(server_socket):
    while True:
        tmp = input()
        if tmp == "exit":
            server_socket.close()
            capture.release()
        break

# 打开摄像头
capture = cv2.VideoCapture(0)

# 创建一个TCP服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_address = ('0.0.0.0', 8000)
server_socket.bind(server_address)

# 开始监听客户端连接
server_socket.listen(1)  # 参数表示最大等待连接数

# 关闭服务器
exit_thread = threading.Thread(target=exit_server, args=(server_socket,))
exit_thread.start()

while True:
    print("等待客户端连接...")
    try:
        client_socket, client_address = server_socket.accept()  # 阻塞，等待客户端连接

    except:
        break
    print("客户端已连接:", client_address)
    handle_client_request(client_socket, client_address,capture,follow)
