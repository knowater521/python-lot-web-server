# -*- coding: utf-8 -*
import os
import time

from RPi import GPIO

from reedSwitch import ReedSwitch


class PhotoelectricSensor(object):
    """
    光电传感器
    用于记录位置，locationTotal总共这么多个埋点位置
    """

    def __init__(self, photoelectricSensorPin, initPin, reedSwitch, relayLeft, relayRight, locationTotal):
        """

        :param photoelectricSensorPin: U型光电传感器串口位置
        :param locationTotal: 总共设定多少个位置
        :param initPin 初始化传感器串口（干簧管传感器pin）

        locationCount 设备所在位置计数
        locationNO 要设置的位置 -1为默认状态， 触发光电时终止继电器
        self.reedSwitch.direction 电机方向
        """
        self.timeFlag = time.time()
        self.timeout = 2
        self.relayLeft = relayLeft
        self.relayRight = relayRight
        self.reedSwitch = reedSwitch
        self.photoelectricSensorPin = photoelectricSensorPin
        self.initPin = initPin
        self.locationTotal = locationTotal
        self.locationCount = 0
        self.locationNO = -1
        self.executing = False

        GPIO.setmode(GPIO.BCM)
        # 设置U型光电传感器为输入模式，上拉电位至3.3V
        GPIO.setup(photoelectricSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        GPIO.add_event_detect(photoelectricSensorPin, GPIO.FALLING, callback=lambda callback: self.__setStatus1(callback),
                              bouncetime=500)

    def __setStatus1(self, callback):
        if (time.time() - self.timeFlag) < self.timeout:
            print "短时间内光电被触发，本次事件不被执行"
            return
        else:
            print "光电传感器被触发，开始执行触发逻辑。。。。。"
            self.timeFlag = time.time()

        # 如果是要指定某一个位置
        if not self.locationNO <= -1:
            self.timeFlag = time.time()
            if self.reedSwitch.direction == "left":
                # 指定向左某个位置
                self.locationCount -= 1
            else:
                # 指定向右某个位置
                self.locationCount += 1
            print "指定位置：", self.locationNO, "现已到达：", self.locationCount
            if self.locationCount == self.locationNO:
                # 到达指定位置
                self.relayLeft.setHigh()
                self.relayRight.setHigh()
                self.executing = False
                self.locationNO = -1
                print "位置已经到达：", self.locationCount, "指定位置参数locationNO初始化完成，释放继电器控制"

        else:
            print "光电传感器被触发到下一个位置！触发前位置：", self.locationCount, "电机当前执行方向：", self.reedSwitch.direction
            self.relayLeft.setHigh()
            self.relayRight.setHigh()
            self.executing = False
            if self.reedSwitch.direction == "left":
                # 向左行驶，位置-1
                self.locationCount -= 1
            else:
                # 向右行驶，位置+1
                self.locationCount += 1

    def __setStatus(self, callback):
        if (time.time() - self.timeFlag) < self.timeout:
            print "短时间内光电被触发，本次事件不被执行"
            return
        else:
            print self.timeout, "timeout", self.timeFlag, "timeflag", time.time(), "Now"
            self.timeFlag = time.time()
        # os.system('clear')  # verlangsamt die Bewegung des Motors zu sehr.
        print "电机运行方向：", self.reedSwitch.direction, "U型光电被触发,之前位置：", self.locationCount
        if self.reedSwitch.direction == "left":

            if self.locationCount > 1:
                self.locationCount -= 1
                if self.locationNO == -1:
                    self.relayLeft.setHigh()
                    self.relayRight.setHigh()
            if self.locationCount <= 1:
                if self.locationNO == -1:
                    self.relayLeft.setHigh()
                    self.relayRight.setHigh()
                else:
                    self.relayLeft.setHigh()
                    self.relayRight.setLow()
                self.locationCount = 1
                self.reedSwitch.direction = "right"
        else:
            if self.locationCount < self.locationTotal:
                self.locationCount += 1
                if self.locationNO == -1:
                    self.relayLeft.setHigh()
                    self.relayRight.setHigh()
            if self.locationCount >= self.locationTotal:
                if self.locationNO == -1:
                    self.relayLeft.setHigh()
                    self.relayRight.setHigh()
                else:
                    self.relayRight.setHigh()
                    self.relayLeft.setLow()
                self.locationCount = self.locationTotal
                self.reedSwitch.direction = "left"

        print "locationNO:", self.locationNO

        if self.locationNO > 0:
            print "self.locationNO == self.locationCount", self.locationNO, self.locationCount,\
                self.locationNO == self.locationCount
            if self.locationNO == self.locationCount:
                self.relayLeft.setHigh()
                self.relayRight.setHigh()
                self.locationNO = -1

        print "U型光电当前所在位置：", self.locationCount

    def specifiedLocation(self, locationNO):
        self.relayLeft.setHigh()
        self.relayRight.setHigh()
        print "要设置的位置：", locationNO, "当前所在位置：", self.locationCount
        if locationNO > 7:
            locationNO = 7
        if locationNO < 0:
            locationNO = 0
        if locationNO == self.locationCount:
            return "当前就在该位置，不需要移动"

        self.locationNO = locationNO

        time.sleep(1)
        if self.locationNO > self.locationCount:
            self.reedSwitch.direction = "right"
        if self.locationNO < self.locationCount:
            self.reedSwitch.direction = "left"

        if self.reedSwitch.direction == "left":
            self.relayLeft.setLow()
        if self.reedSwitch.direction == "right":
            self.relayRight.setLow()
        return "当前设备位置", self.locationCount, "将向", self.reedSwitch.direction, "移动到", self.locationNO

    def uninstall(self):
        """
        卸载光电传感器
        :return:
        """
        print "卸载光电传感器"
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        self.locationCount = 0
        self.locationNO = -1
        self.reedSwitch.direction = "left"
        print "光电传感器已卸载，电机向左行驶"
        pass

    def install(self):
        """
        初始化光电传感器
        :return:
        """
        print "初始化电传感器"
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        GPIO.add_event_detect(self.photoelectricSensorPin, GPIO.FALLING,
                              callback=lambda callback: self.__setStatus1(callback),
                              bouncetime=500)
        print "光电传感器重新注册成功"

