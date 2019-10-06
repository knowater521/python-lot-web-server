# -*- coding: utf-8 -*
from time import sleep

import RPi.GPIO as GPIO


class Motor(object):
    """
    控制电机的旋转，向电机输入脉冲信号，8个脉冲信号是一个循环，a-ab-b-bc-c-cd-d-da
    """
    def __init__(self, IN1, IN2, IN3, IN4, time=0.001):
        """
        :param IN1: 电机针脚
        :param IN2: 电机针脚
        :param IN3: 电机针脚
        :param IN4: 电机针脚
        :param time: 电机脉冲间歇时间默认0.001
        """
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.time = time
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)

        self.status = False

    def step1(self):
        GPIO.output(self.IN4, True)
        sleep(self.time)
        GPIO.output(self.IN4, False)

    def step2(self):
        GPIO.output(self.IN4, True)
        GPIO.output(self.IN3, True)
        sleep(self.time)
        GPIO.output(self.IN4, False)
        GPIO.output(self.IN3, False)

    def step3(self):
        GPIO.output(self.IN3, True)
        sleep(self.time)
        GPIO.output(self.IN3, False)

    def step4(self):
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, True)
        sleep(self.time)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)

    def step5(self):
        GPIO.output(self.IN2, True)
        sleep(self.time)
        GPIO.output(self.IN2, False)

    def step6(self):
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, True)
        sleep(self.time)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)

    def step7(self):
        GPIO.output(self.IN1, True)
        sleep(self.time)
        GPIO.output(self.IN1, False)

    def step8(self):
        GPIO.output(self.IN4, True)
        GPIO.output(self.IN1, True)
        sleep(self.time)
        GPIO.output(self.IN4, False)
        GPIO.output(self.IN1, False)

    def left(self):
        # os.system('clear') # verlangsamt die Bewegung des Motors zu sehr.
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()
        self.step7()
        self.step8()

    def right(self):
        # os.system('clear') # verlangsamt die Bewegung des Motors zu sehr.
        self.step8()
        self.step7()
        self.step6()
        self.step5()
        self.step4()
        self.step3()
        self.step2()
        self.step1()
