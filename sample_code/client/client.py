import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from client_utils.utils import *

import threading
import torch
print(f'torch版本：{torch.__version__}')

import sys
from datetime import datetime


class LogEmitter(QObject):
    log_message_signal = pyqtSignal(str)

    def log_message(self, message):
        # 在子线程中发射信号
        self.log_message_signal.emit(message)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        print('开始加载模型')
        self.model = torch.hub.load('D:\\courseDesignIV\\yolov5-master', 'custom',
                               'E:\\wechat\\WeChat Files\\WeChat Files\\wxid_48i6imreba7f22\\FileStorage\\File\\2024-01\\best.pt',
                               source='local')
        self.model.conf = 0.30  # NMS confidence threshold
        #.iou = 0.5
        # model = model.cuda(0)
        print('加载模型完成')

        # 是否开始任务
        self.hasDoing = False
        # 是否已经断开连接
        self.hasDiscon = True

        # 初始化UI布局
        self.init_ui()
        # 初始化UI连接
        self.init_UIconn()


    def init_ui(self):
        # 创建垂直布局
        v_layout = QVBoxLayout()

        # 创建label
        self.lab_vid = QLabel('this is Label')
        self.lab_vid.setAlignment(Qt.AlignCenter)
        self.lab_vid.setMinimumSize(640, 480)

        # 创建水平布局
        h_layout_btn = QHBoxLayout()
        h_layout_lab = QHBoxLayout()

        # 创建按钮
        self.btn_connect = QPushButton('Connect')
        self.btn_disconnect = QPushButton('Disconnect')
        self.btn_disconnect.setDisabled(True)

        # 创建日志文本框
        self.log_text_edit = QPlainTextEdit(self)
        self.log_text_edit.setReadOnly(True)  # 设置为只读，用于显示日志信息

        self.log_emitter = LogEmitter()
        self.log_emitter.log_message_signal.connect(self.log_message)

        # 将按钮和文本框添加到布局中
        v_layout.addLayout(h_layout_lab)
        v_layout.addLayout(h_layout_btn)

        h_layout_btn.addWidget(self.btn_connect)
        h_layout_btn.addWidget(self.btn_disconnect)

        h_layout_lab.addWidget(self.lab_vid)
        h_layout_lab.addWidget(self.log_text_edit)

        # 将垂直布局设置为主widget的布局
        self.setLayout(v_layout)

        self.setGeometry(300, 200, 1280, 720)
        self.setMinimumSize(640, 480)
        self.setWindowTitle('基于YOLOv5的机械臂交互系统')
        self.show()


    def init_UIconn(self):
        self.btn_connect.clicked.connect(self.connect_server)
        self.btn_disconnect.clicked.connect(self.disconnect_server)
        
        
    def closeEvent(self, event):
            # 重写关闭窗口事件
            reply = QMessageBox.question(self, '确认退出', '确定要退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
                # 关闭连接
                self.hasDoing = False
            else:
                event.ignore()


    # 打印日志
    def log_paint(self, message):
        QCoreApplication.postEvent(self.edit_log, LogEvent(message))

        
    def log_message(self, message):
        # 在主线程中更新 UI
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.log_text_edit.appendPlainText(formatted_datetime + " " + message)


    def begin_task(self):
        task = 'task1'
        # 创建一个TCP客户端套接字
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 服务器地址和端口
        server_address = ('192.168.1.21', 8000)
        # 连接服务器
        self.log_emitter.log_message("开始连接服务器")
        client_socket.connect(server_address)
        self.log_emitter.log_message("服务器连接完毕")

        self.hasDiscon = False
        while self.hasDoing:
            send_server_request(self, client_socket, task, self.model)
        # 如果task_flag = False 关闭连接
        client_socket.close()
        self.hasDiscon = True
        

    def connect_server(self):
        # 如果没有断开连接，跳过
        if self.hasDiscon == False:
            return
        self.log_emitter.log_message("点击开始连接服务器")
        self.hasDoing = True
        # 开启线程处理任务
        task_thread = threading.Thread(target=self.begin_task, )
        task_thread.start()
        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)


    def disconnect_server(self):
        # 如果断开了连接，跳过
        if self.hasDiscon == True:
            return
        self.log_emitter.log_message("点击断开连接服务器")
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)        
        self.hasDoing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
