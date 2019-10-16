# coding=utf-8
import time

from RPi import GPIO

from button import Button
from motor import Motor
from photoelectricSensor import PhotoelectricSensor
from reedSwitch import ReedSwitch
from relay import Relay


class ControlMotor(object):
    def __init__(self, IN1, IN2, IN3, IN4, reedSwitchPin, relay1Pin, relay2Pin, photoelectricSensorPin
                 , locationTotal=7, initPosition="left"):
        self.initPosition = initPosition
        self.locationTotal = locationTotal
        self.photoelectricSensorPin = photoelectricSensorPin

        self.relay2Pin = relay2Pin
        self.relay1Pin = relay1Pin
        self.reedSwitchPin = reedSwitchPin
        self.IN4 = IN4
        self.IN3 = IN3
        self.IN2 = IN2
        self.IN1 = IN1

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # motor = Motor(17, 16, 13, 12)
        # self.motor = Motor(IN1, IN2, IN3, IN4)
        # 左转继电器relay1 = Relay(18)
        self.relayLeft = Relay(relay1Pin)
        # 右转继电器relay2 = Relay(19)
        self.relayRight = Relay(relay2Pin)

        # 干簧管传感器 reedSwitch = ReedSwitch(20, relay1, relay2)
        self.reedSwitch = ReedSwitch(reedSwitchPin, self.relayLeft, self.relayRight, initPosition)

        # 光电传感器PhotoelectricSensor(5, reedSwitch.reedSwitchPin, reedSwitch, relay1, relay2)
        self.photoelectricSensor = PhotoelectricSensor(photoelectricSensorPin, self.reedSwitch.reedSwitchPin,
                                                       self.reedSwitch, self.relayLeft, self.relayRight, locationTotal)

        print("初始化继电器开，方向：", initPosition)
        self.init_motor()
        print("设备初始完成")

    def init_motor(self):
        """
        开机启动，程序向右执行5s
        停止继电器输出
        继电器向左行驶，直到干簧管传感器低电位
        继电器向右行驶，直到光电传感器被触发
        :return:
        """
        self.relayStop()
        GPIO.remove_event_detect(self.photoelectricSensorPin)
        GPIO.remove_event_detect(self.reedSwitchPin)

        timeFlag = time.time()
        if self.reedSwitch.initDirection == "left":
            print("初始化--向右离开初始位置")
            self.reedSwitch.direction = "right"
            self.relayStart()
            time.sleep(5)
            print("初始化--向左回到初始位置")
            self.relayStop()
            self.reedSwitch.direction = "left"
            self.relayStart()
            print("初始化--当前干簧管状态" + str(GPIO.input(self.reedSwitchPin)))
            while GPIO.input(self.reedSwitchPin) == GPIO.HIGH and time.time() - timeFlag < 5000:
                pass
            print("初始化--到达初始位置")
            self.relayStop()
            print("初始化--开始向右行驶到0位置，当前光电状态" + str(GPIO.input(self.photoelectricSensorPin)))
            self.reedSwitch.direction = "right"
            self.relayStart()
            while GPIO.input(self.photoelectricSensorPin) == GPIO.LOW and time.time() - timeFlag < 5000:
                pass
            print("初始化--到达0位置，初始化结束")
            self.relayStop()
        else:
            self.reedSwitch.direction = "left"
            self.relayStart()
            time.sleep(5)
            self.relayStop()
            self.reedSwitch.direction = "right"
            self.relayStart()
            while GPIO.input(self.reedSwitchPin) == GPIO.HIGH and time.time() - timeFlag < 5000:
                pass
            self.relayStop()
            self.reedSwitch.direction = "left"
            self.relayStart()
            while GPIO.input(self.photoelectricSensorPin) == GPIO.LOW and time.time() - timeFlag < 5000:
                pass
            self.relayStop()
        self.photoelectricSensor.executing = False
        self.photoelectricSensor.locationCount = 0
        self.photoelectricSensor.locationNO = -1
        self.photoelectricSensor.timeFlag = time.time()
        GPIO.add_event_detect(self.reedSwitchPin, GPIO.BOTH,
                              callback=lambda callback: self.setStatus(callback), bouncetime=200)
        GPIO.add_event_detect(self.photoelectricSensorPin, GPIO.FALLING,
                              callback=lambda callback: self.photoelectricSensor.setStatus1(callback), bouncetime=500)

    def relayStart(self):
        if self.photoelectricSensor.executing:
            return "设备正在被执行中，请稍后再试"
        if self.reedSwitch.direction == "left":
            print("左继电器开")
            self.photoelectricSensor.executing = True
            self.relayRight.setHigh()
            self.relayLeft.setLow()
        else:
            print("右继电器开")
            self.photoelectricSensor.executing = True
            self.relayLeft.setHigh()
            self.relayRight.setLow()

    def relayStop(self):
        self.relayRight.setHigh()
        self.relayLeft.setHigh()
        self.photoelectricSensor.executing = False
        return "设备已终止执行！"

    def setStatus(self, callback):
        print ("干簧管被触发")
        self.relayRight.setHigh()
        self.relayLeft.setHigh()
        self.photoelectricSensor.executing = False

    # def init_motor1(self):
    #     """
    #     原来的初始化方式
    #     :return:
    #     """
    #     if self.reedSwitch.direction == "left":
    #         self.reedSwitch.direction = "right"
    #         self.relayLeft.setHigh()
    #         self.relayRight.setLow()
    #         time.sleep(5)
    #         self.reedSwitch.direction = "left"
    #         self.relayRight.setHigh()
    #         self.relayLeft.setLow()
    #         time.sleep(15)
    #         self.relayLeft.setHigh()
    #         self.relayRight.setHigh()
    #     else:
    #         self.reedSwitch.direction = "left"
    #         self.relayRight.setHigh()
    #         self.relayLeft.setLow()
    #         time.sleep(5)
    #         self.reedSwitch.direction = "right"
    #         self.relayLeft.setHigh()
    #         self.relayRight.setLow()
    #         time.sleep(15)
    #         self.relayLeft.setHigh()
    #         self.relayRight.setHigh()
