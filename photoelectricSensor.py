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
        :param initPin 初始化传感器串口
        """
        self.relayLeft = relayLeft
        self.relayRight = relayRight
        self.reedSwitch = reedSwitch
        self.initPin = initPin
        self.locationTotal = locationTotal
        self.locationCount = 0
        self.photoelectricSensorPin = photoelectricSensorPin
        GPIO.setmode(GPIO.BCM)
        # 设置U型光电传感器为输入模式，上拉电位至3.3V
        GPIO.setup(photoelectricSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        GPIO.add_event_detect(photoelectricSensorPin, GPIO.BOTH, callback=lambda callback: self.__setStatus(callback),
                              bouncetime=200)
        self.locationNO = -1

    def __setStatus(self, callback):
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
        print "要设置的位置：", locationNO
        if locationNO == self.locationCount:
            return self.locationCount, self.reedSwitch.direction
        self.locationNO = locationNO
        self.relayLeft.setHigh()
        self.relayRight.setHigh()
        time.sleep(1)

        if self.reedSwitch.direction == "left":
            if locationNO > self.locationCount:
                self.reedSwitch.direction = "right"
            self.relayLeft.setLow()
        else:
            if locationNO < self.locationCount:
                self.reedSwitch.direction = "left"
            self.relayRight.setLow()
        return self.locationCount, self.reedSwitch.direction

