import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QTimer

class LogEmitter(QObject):
    log_message_signal = pyqtSignal(str)

    def log_message(self, message):
        # 在子线程中发射信号
        self.log_message_signal.emit(message)

class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口
        self.setWindowTitle("Log Viewer")
        self.setGeometry(100, 100, 600, 400)

        # 创建日志文本框
        self.log_text_edit = QPlainTextEdit(self)
        self.log_text_edit.setReadOnly(True)  # 设置为只读，用于显示日志信息

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.log_text_edit)

        # 创建主 Widget，并设置布局
        main_widget = QWidget()
        main_widget.setLayout(layout)

        # 将主 Widget 设置为主窗口的中央 Widget
        self.setCentralWidget(main_widget)

        # 创建 LogEmitter 实例，并连接信号与槽
        self.log_emitter = LogEmitter()
        self.log_emitter.log_message_signal.connect(self.log_message)

        # 创建一个定时器，模拟子线程中产生的日志消息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.emit_log_message)
        self.timer.start(1000)

    def emit_log_message(self):
        # 模拟子线程中产生的日志消息
        log_message = "This is a log message."
        self.log_emitter.log_message(log_message)

    def log_message(self, message):
        # 在主线程中更新 UI
        self.log_text_edit.appendPlainText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()

    sys.exit(app.exec_())
