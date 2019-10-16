# -*- coding: utf-8 -*
import time

from RPi import GPIO


class Button(object):

    def __init__(self, btnPin, reedSwitchPin, motor, reedSwitch):
        self.reedSwitch = reedSwitch
        self.reedSwitchPin = reedSwitchPin
        self.motor = motor
        print ("初始化btn", btnPin)
        self.btnPin = btnPin
        GPIO.setmode(GPIO.BCM)
        # 设置干簧管为输入模式，上拉电位至3.3V
        GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.btnPin)
        self.status = False
        GPIO.add_event_detect(btnPin, GPIO.BOTH, callback=lambda callback: self.__setStatus(callback), bouncetime=200)

    def __setStatus(self, callback):
        print ("继电器被改变：", self.btnPin, GPIO.input(self.btnPin))
        if self.status:
            self.status = False
        else:
            self.status = True
        while GPIO.input(self.btnPin) == 0 and GPIO.input(self.reedSwitchPin) == 1:
            if self.reedSwitch.direction == "left":
                self.motor.left()
            else:
                self.motor.right()
        print ("电机停止", self.direction,  "旋转")
