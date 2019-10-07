# -*- coding: utf-8 -*
import time

from RPi import GPIO


class ReedSwitch(object):
    """
    干簧管传感器
    用于检测设备初始位置和确定运行方向
    """

    def __init__(self, reedSwitchPin, relayLeft, relayRight, initDirection="left"):
        self.relayRight = relayRight
        self.relayLeft = relayLeft
        print "初始化干簧管监听器"
        self.reedSwitchPin = reedSwitchPin
        GPIO.setmode(GPIO.BCM)
        # 设置干簧管为输入模式，上拉电位至3.3V
        GPIO.setup(reedSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.reedSwitchPin)
        GPIO.add_event_detect(reedSwitchPin, GPIO.BOTH, callback=lambda callback: self.setStatus(callback),
                              bouncetime=200)
        self.status = False
        self.direction = initDirection

    def setStatus(self, callback):
        print "干簧管状态变更:", GPIO.input(self.reedSwitchPin), "原状态status:", self.status
        self.status = GPIO.input(self.reedSwitchPin) == 1
        self.relayRight.setHigh()
        self.relayLeft.setHigh()

    # def __del__(self):
    #     print "释放干簧管针脚资源"
    #     GPIO.cleanup()
