# -*- coding: utf-8 -*
from RPi import GPIO


class PhotoelectricSensor(object):
    """
    光电传感器
    """

    def __init__(self, photoelectricSensorPin, locationTotal, referenceInitPin, controlMotor):
        """

        :param photoelectricSensorPin: U型光电传感器串口位置
        :param locationTotal: 总共设定多少个位置
        :param referenceInitPin 初始状态参考串口位置
        """
        self.controlMotor = controlMotor
        self.locationTotal = locationTotal
        self.photoelectricSensorPin = photoelectricSensorPin
        self.referenceInitPin = referenceInitPin
        GPIO.setmode(GPIO.BCM)
        # 设置U型光电传感器为输入模式，上拉电位至3.3V
        GPIO.setup(photoelectricSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        self.status = False
        self.locationCount = 1
        GPIO.add_event_detect(photoelectricSensorPin, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_callback(photoelectricSensorPin, callback=lambda callback: self.__setStatus(callback))
        GPIO.add_event_callback(referenceInitPin, callback=lambda callback: self.__setLocationCount(callback))

    def __setStatus(self, callback):
        if self.status:
            self.status = False
        else:
            self.status = True

        print "U型光电被触发,之前位置：", self.locationCount
        if self.controlMotor.doubleClickFlag:
            self.locationCount -= 1
            if 0 == self.locationCount:
                self.locationCount = self.locationTotal
        else:
            self.locationCount += 1
            if self.locationTotal < self.locationCount:
                self.locationCount = 1
        print "U型光电被触发,当前位置：", self.locationCount

    def __setLocationCount(self, callback):
        print "检测到达初始位置，当前位置：", self.locationCount, "设置位置为1"
        self.locationCount = 1

    def getLevel(self):
        return GPIO.input(self.photoelectricSensorPin)
