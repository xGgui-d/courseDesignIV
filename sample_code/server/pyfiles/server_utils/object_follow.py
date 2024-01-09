# !/usr/bin/env python
# coding: utf-8

#从当前包中导入PID
from . import PID
import Arm_Lib


class object_follow:
    def __init__(self):
        self.Arm = Arm_Lib.Arm_Device()
        self.target_servox = 90
        self.target_servoy = 45
        self.xservo_pid = PID.PositionalPID(0.5, 0.2, 0.31)
        self.yservo_pid = PID.PositionalPID(0.5, 0.2, 0.35)
        # Create an instance of OpenCV's joint classifier
        # 创建opencv的联级分类器的实例

    def follow_function(self, point_x, point_y):

        if not (self.target_servox >= 180 and point_x <= 320 or self.target_servox <= 0 and point_x >= 320):
            self.xservo_pid.SystemOutput = point_x
            self.xservo_pid.SetStepSignal(320)
            self.xservo_pid.SetInertiaTime(0.01, 0.1)
            target_valuex = int(1500 + self.xservo_pid.SystemOutput)
            self.target_servox = int((target_valuex - 500) / 10)
            # Set movement restrictions
            # 设置移动限制
            if self.target_servox > 180: self.target_servox = 180
            if self.target_servox < 0: self.target_servox = 0
        if not (self.target_servoy >= 180 and point_y <= 240 or self.target_servoy <= 0 and point_y >= 240):
            # Input Y-axis direction parameter PID control input
            # 输入Y轴方向参数PID控制输入
            self.yservo_pid.SystemOutput = point_y
            self.yservo_pid.SetStepSignal(240)
            self.yservo_pid.SetInertiaTime(0.01, 0.1)
            target_valuey = int(1500 + self.yservo_pid.SystemOutput)
            self.target_servoy = int((target_valuey - 500) / 10) - 45
            # Set movement restrictions
            # 设置移动限制
            if self.target_servoy > 360: self.target_servoy = 360
            if self.target_servoy < 0: self.target_servoy = 0
        joints_0 = [self.target_servox, 135, self.target_servoy / 2, self.target_servoy / 2, 90, 30]
        self.Arm.Arm_serial_servo_write6_array(joints_0, 300)
