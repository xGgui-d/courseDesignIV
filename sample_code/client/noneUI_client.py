from client_utils.utils import *
import threading
import torch

print(torch.__version__)

task_flag = True
main_flag = True
print("开始加载模型！")
model = torch.hub.load('D:\\courseDesignIV\\yolov5-master\\yolov5-master', 'custom', 'E:\\wechat\\WeChat Files\\WeChat Files\\wxid_48i6imreba7f22\\FileStorage\\File\\2024-01\\best.pt', source='local')
# model.conf = 0.7  # NMS confidence threshold
#.iou = 0.5
# model = model.cuda(0)
print("模型加载完成！")
print("input a task:[task]")



def begin_task(model):
    task = 'task1'

    # 创建一个TCP客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 服务器地址和端口
    server_address = ('192.168.159.144', 8000)
    # 连接服务器
    print('开始连接服务器')
    client_socket.connect(server_address)
    print('连接完毕')
    while task_flag:
        send_server_request(client_socket, task, model)
    client_socket.close()


while main_flag:
    order = input()
    if order == "task":
        task_flag = True
        task_thread = threading.Thread(target=begin_task, args=(model,))
        task_thread.start()

    elif order == "e":
        # 关闭连接
        task_flag = False
    elif order == "q":
        # 关闭程序
        main_flag = False
