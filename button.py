# -*- coding: utf-8 -*
import time

from RPi import GPIO


class Button(object):

    def __init__(self, btnPin):
        self.btnPin = btnPin
        GPIO.setmode(GPIO.BCM)
        # 设置干簧管为输入模式，上拉电位至3.3V
        GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.btnPin)
        self.status = False
        GPIO.add_event_detect(btnPin, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_callback(btnPin, callback=lambda callback: self.__setStatus(callback))

    def __setStatus(self, callback):
        if self.status:
            self.status = False
        else:
            self.status = True
