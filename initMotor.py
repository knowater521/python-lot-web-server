# -*- coding: utf-8 -*
from RPi import GPIO

from motor import Motor
from reedSwitch import ReedSwitch
import time


class InitMotor(Motor):
    """
    电机运行的初始化
    """
    initMassage = ""

    def __init__(self, IN1, IN2, IN3, IN4, reedSwitchPin, sleep, timeout=50):
        """

        :param IN1:
        :param IN2:
        :param IN3:
        :param IN4:
        :param reedSwitchPin:
        :param sleep: 脉冲信号间隔时间
        :param timeout: 初始化超时时间 秒
        """

        print "初始化电机参数"
        super(InitMotor, self).__init__(IN1, IN2, IN3, IN4, sleep)
        self.timeout = timeout
        print "加载干簧管传感器"
        self.reedSwitch = ReedSwitch(reedSwitchPin)
        print "初始化设备位置"
        self.initMotor()
        print "设备位置初始化位置结束"

    def initMotor(self):
        print "设备位置初始化开始"
        reedSwitch = self.reedSwitch
        reedSwitch.status = False
        startTime = time.time()
        while not reedSwitch.status:
            self.left()
            if self.timeoutM(startTime):
                self.setLed(24)
                self.initMassage = "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
                return False, "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
        print "到达设备初始位置附近"
        flag = False
        for x in range(1, 150):
            self.left()
            time.sleep(0.005)
            if not reedSwitch.status:
                for y in range(x / 2):
                    self.right()
                    time.sleep(0.01)
                flag = True
                break

        if not flag:
            print "没有到达预设位置，再次寻找.."

            reedSwitch.status = False
            while not reedSwitch.status:
                self.left()
                if self.timeoutM(startTime):
                    self.setLed(24)
                    self.initMassage = "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
                    return False, "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
            print "到达设备初始位置附近"
            for x in range(1, 200):
                self.left()
                time.sleep(0.01)
                if not reedSwitch.status:
                    for y in range(x / 2):
                        self.right()
                        time.sleep(0.01)
                    break
        self.initMassage = "初始化成功"
        self.setLed(23)
        return True

    def setLed(self, LED_PIN):
        GPIO.output(LED_PIN, GPIO.HIGH)

    def timeoutM(self, startTime):
        return (time.time() - startTime) > self.timeout

    def __del__(self):
        print "电机控制类被销毁，终止电机IO输出：", self.IN1, self.IN2, self.IN3, self.IN4
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, False)
        print "清理GPIO GPIO.cleanup()"
        GPIO.cleanup()


class ControlMotor(object):
    def __init__(self, IN1, IN2, IN3, IN4, reedSwitchPin, sleep=0.001, timeout=50):
        self.motor = InitMotor(IN1, IN2, IN3, IN4, reedSwitchPin, sleep, timeout)
        self.initMotorMessage = self.motor.initMassage
        print "初始化结果：", self.initMotorMessage

    def leftPosition(self):
        self.motor.left()
        return "左边"

    def rightPosition(self):
        self.motor.right()
        return "右边"
