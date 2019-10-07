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
        self.motor = Motor(IN1, IN2, IN3, IN4)
        # 左转继电器relay1 = Relay(18)
        self.relayLeft = Relay(relay1Pin)
        # 右转继电器relay2 = Relay(19)
        self.relayRight = Relay(relay2Pin)

        # 干簧管传感器 reedSwitch = ReedSwitch(20, relay1, relay2)
        self.reedSwitch = ReedSwitch(reedSwitchPin, self.relayLeft, self.relayRight, initPosition)

        print "初始化继电器开，方向：", initPosition
        self.init_motor()
        # 光电传感器PhotoelectricSensor(5, reedSwitch.reedSwitchPin, reedSwitch, relay1, relay2)
        self.photoelectricSensor = PhotoelectricSensor(photoelectricSensorPin, self.reedSwitch.reedSwitchPin,
                                                       self.reedSwitch, self.relayLeft, self.relayRight, locationTotal)

        # 不需要关注这两个，最后只控制继电器
        # Button(24, 20, self.motor, self.reedSwitch)
        # Button(23, 20, self.motor, self.reedSwitch)

    def init_motor(self):

        if self.reedSwitch.direction == "left":
            self.reedSwitch.direction = "right"
            self.relayLeft.setHigh()
            self.relayRight.setLow()
            time.sleep(5)
            self.reedSwitch.direction = "left"
            self.relayRight.setHigh()
            self.relayLeft.setLow()
            time.sleep(15)
            self.relayLeft.setHigh()
            self.relayRight.setHigh()
        else:
            self.reedSwitch.direction = "left"
            self.relayRight.setHigh()
            self.relayLeft.setLow()
            time.sleep(5)
            self.reedSwitch.direction = "right"
            self.relayLeft.setHigh()
            self.relayRight.setLow()
            time.sleep(15)
            self.relayLeft.setHigh()
            self.relayRight.setHigh()

