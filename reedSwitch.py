# -*- coding: utf-8 -*
from RPi import GPIO


class ReedSwitch(object):
    """干簧管传感器"""
    status = False

    def __init__(self, ReedSwitchPin):
        print "初始化干簧管监听器"
        self.ReedSwitchPin = ReedSwitchPin
        GPIO.setmode(GPIO.BCM)
        # 设置干簧管为输入模式，上拉电位至3.3V
        GPIO.setup(ReedSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.ReedSwitchPin)
        GPIO.add_event_detect(ReedSwitchPin, GPIO.BOTH, callback=lambda callback: self.__setStatus(callback),
                              bouncetime=1)

    def __setStatus(self, callback):
        # print "干簧管状态变更:", GPIO.input(self.ReedSwitchPin), "原状态status:", self.status
        self.status = GPIO.input(self.ReedSwitchPin) == 1

    def reedSwitchOn(self):
        return GPIO.input(self.ReedSwitchPin) == 1

    def reedSwitchOff(self):
        return GPIO.input(self.ReedSwitchPin) == 0

    def __del__(self):
        print "释放干簧管针脚资源"
        GPIO.cleanup()
