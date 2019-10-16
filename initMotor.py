# -*- coding: utf-8 -*

from RPi import GPIO

from button import Button
from motor import Motor
from photoelectricSensor import PhotoelectricSensor
from reedSwitch import ReedSwitch
import time


def setLed(LED_PIN):
    GPIO.output(LED_PIN, GPIO.HIGH)


def setLedOff(LED_PIN):
    GPIO.output(LED_PIN, GPIO.LOW)


class InitMotor(Motor):
    """
    电机运行的初始化
    """
    initMassage = ""

    def __init__(self, IN1, IN2, IN3, IN4, reedSwitchPin, btnPin, sleep, timeout=50):
        """

        :param IN1:
        :param IN2:
        :param IN3:
        :param IN4:
        :param reedSwitchPin: 干簧管pin
        :param sleep: 脉冲信号间隔时间
        :param timeout: 初始化超时时间 秒
        :param btnPin 急停按键
        """

        self.timeout = timeout
        print ("加载干簧管传感器")
        self.reedSwitch = ReedSwitch(reedSwitchPin)
        print ("加载按键")
        self.btn = Button(btnPin)
        print ("初始化电机参数")
        super(InitMotor, self).__init__(IN1, IN2, IN3, IN4, sleep)
        print ("初始化设备位置")
        self.initMotor()
        print ("设备位置初始化位置结束")

    def initMotor(self):
        if self.status:
            setLed(24)
            self.initMassage = "电机：", self.IN1, self.IN2, self.IN3, self.IN4, "检测到正在被执行中，请稍后，若无运转请检查设备是否异常！"
            return False, "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
        else:
            self.status = True
        btnStatus = self.btn.status
        print ("当前按键状态：", btnStatus)
        print ("设备位置初始化开始")
        reedSwitch = self.reedSwitch
        reedSwitch.status = False
        startTime = time.time()
        while not reedSwitch.status:
            if self.btn.status != btnStatus:
                setLed(25)
                self.initMassage = "设备初始化被手动终止"
                return False, "设备初始化被手动终止"
            self.left()
            if self.timeoutM(startTime):
                setLed(24)
                self.initMassage = "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
                return False, "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
        print ("到达设备初始位置附近")
        flag = False
        for x in range(1, 150):
            if self.btn.status != btnStatus:
                setLed(25)
                self.initMassage = "设备初始化被手动终止"
                return False, "设备初始化被手动终止"
            self.left()
            # time.sleep(0.005)
            if not reedSwitch.status:
                for y in range(x / 2):
                    if self.btn.status != btnStatus:
                        setLed(25)
                        self.initMassage = "设备初始化被手动终止"
                        return False, "设备初始化被手动终止"
                    self.right()
                    # time.sleep(0.01)
                flag = True
                break

        if not flag:
            print ("没有到达预设位置，再次寻找..")

            reedSwitch.status = False
            while not reedSwitch.status:
                if self.btn.status != btnStatus:
                    setLed(25)
                    self.initMassage = "设备初始化被手动终止"
                    return False, "设备初始化被手动终止"
                self.left()
                if self.timeoutM(startTime):
                    setLed(24)
                    self.initMassage = "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
                    return False, "设备初始化超时，请检查1号传感器组合状态或1号电机有无正常运转"
            print ("到达设备初始位置附近")
            for x in range(1, 200):
                if self.btn.status != btnStatus:
                    setLed(25)
                    self.initMassage = "设备初始化被手动终止"
                    return False, "设备初始化被手动终止"
                self.left()
                # time.sleep(0.01)
                if not reedSwitch.status:
                    for y in range(x / 2):
                        if self.btn.status != btnStatus:
                            setLed(25)
                            self.initMassage = "设备初始化被手动终止"
                            return False, "设备初始化被手动终止"
                        self.right()
                        # time.sleep(0.01)
                    break
        self.initMassage = "初始化成功"
        setLed(23)
        return True

    def timeoutM(self, startTime):
        return (time.time() - startTime) > self.timeout

    def __del__(self):
        print ("电机控制类被销毁，终止电机IO输出：", self.IN1, self.IN2, self.IN3, self.IN4)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, False)
        print ("清理GPIO GPIO.cleanup()")
        GPIO.cleanup()


class ControlMotor1(object):
    def __init__(self, IN1, IN2, IN3, IN4, reedSwitchPin, btnPin, photoelectricSensorPin, locationTotal, sleep=0.001,
                 timeout=50):
        self.motor = InitMotor(IN1, IN2, IN3, IN4, reedSwitchPin, btnPin, sleep, timeout)
        self.motor.status = False
        self.doubleClickFlag = False
        self.initMotorMessage = self.motor.initMassage
        self.btnPin = btnPin
        self.doubleClickTimeFlag = 0
        print ("初始化结果：", self.initMotorMessage)
        print ("加载手动调整电机")
        GPIO.add_event_callback(btnPin, callback=lambda callback: self.__controlMotor(callback))
        GPIO.add_event_callback(btnPin, callback=lambda callback: self.__doubleClick(callback))
        print ("加载U型光电传感器")
        self.photoelectricSensor = PhotoelectricSensor(photoelectricSensorPin, locationTotal, reedSwitchPin, self)

    def leftPosition(self):
        self.motor.left()
        return "左边"

    def rightPosition(self):
        self.motor.right()
        return "右边"

    def __controlMotor(self, callback):
        if not self.motor.status:
            setLed(25)
            self.motor.status = True
            self.doubleClickTimeFlag = time.time()
            while GPIO.input(self.btnPin) == 0:
                if self.doubleClickFlag:
                    # print ("向右旋转", time.time()
                    self.motor.right()
                else:
                    # print ("向左旋转", time.time()
                    self.motor.left()

            self.motor.status = False
            setLedOff(25)
        # status = GPIO.input(self.ReedSwitchPin)

    def __doubleClick(self, callback):
        result = 0
        for i in range(200):
            time.sleep(0.001)
            pinStat = GPIO.input(self.btnPin)
            if pinStat == GPIO.LOW and result == 0:
                result = 1
            timeCount = time.time() - self.doubleClickTimeFlag
            if result == 1 and pinStat == GPIO.HIGH and 0.3 > timeCount > 0.1:
                result = 2
                print ("设置左右转")
                if self.doubleClickFlag:
                    setLed(24)
                    time.sleep(0.15)
                    setLedOff(24)
                    self.doubleClickFlag = False
                else:
                    setLed(24)
                    time.sleep(0.15)
                    setLedOff(24)
                    self.doubleClickFlag = True
                return result
        return 3
