# -*- coding: utf-8 -*
"""
滑轨控制
"""
import os
import time

import RPi.GPIO as GPIO
from flask import Flask, json

from controlMotor import ControlMotor

app = Flask(__name__)

controlMotor = ControlMotor(17, 16, 13, 12, 20, 18, 19, 5, 7)


@app.route("/")
def main():

    return "主页"


def setRelay(changePin, action):
    """

    :param changePin: 要开启继电器的针脚编号18，19
    :param action:
    :return:
    """
    direction = controlMotor.reedSwitch.direction
    locationCount = controlMotor.photoelectricSensor.locationCount
    print ("当前运行方向" + str(direction) + "当前位置" + str(locationCount))
    changePin = int(changePin)
    if action == "on".lower():
        if controlMotor.photoelectricSensor.executing:
            return "设备正在做其他操作，请稍后再试"
        controlMotor.photoelectricSensor.executing = True
        controlMotor.relayLeft.setHigh()
        controlMotor.relayRight.setHigh()
        if changePin == 18:
            if locationCount > 1:
                controlMotor.reedSwitch.direction = "left"
                controlMotor.relayLeft.setLow()
                print ("左转继电器开启")
            else:
                print ("到达1号或初始位置，不可以继续执行向左操作")
                controlMotor.photoelectricSensor.executing = False
                return "off"
        else:
            if locationCount < 7:
                controlMotor.reedSwitch.direction = "right"
                controlMotor.relayRight.setLow()
                print ("右转继电器开启")
            else:
                print ("到达7号位置，不可以继续执行向右操作")
                controlMotor.photoelectricSensor.executing = False
                return "off"
        return "on"
    if action == "off":
        controlMotor.relayRight.setHigh()
        controlMotor.relayLeft.setHigh()
        controlMotor.photoelectricSensor.executing = False
        controlMotor.photoelectricSensor.locationNO = -1
        return "off"


@app.route("/relay/<changePin>/<action>")
def relayControl(changePin, action):
    controlMotor.photoelectricSensor.timeFlag = time.time()
    templateData = {
        'relayPins': changePin,
        'relayMessage': setRelay(changePin, action)
    }
    return json.dumps(templateData)


@app.route("/left")
def left():
    controlMotor.photoelectricSensor.timeFlag = time.time()
    templateData = {
        'relayPins': 18,
        'relayMessage': setRelay(18, "on")
    }
    return json.dumps(templateData)


@app.route("/right")
def right():
    controlMotor.photoelectricSensor.timeFlag = time.time()
    templateData = {
        'relayPins': 19,
        'relayMessage': setRelay(19, "on")
    }
    return json.dumps(templateData)


@app.route("/stop")
def stop():
    controlMotor.photoelectricSensor.timeFlag = time.time()
    templateData = {
        'relayPins': 1819,
        'relayMessage': setRelay(18, "off")
    }
    return json.dumps(templateData)


@app.route("/specified/<location>")
def specifiedLocation(location):
    if int(location) > 7 or int(location) < 1 or controlMotor.photoelectricSensor.executing:
        templateData = {
            'message': "只能选择1-7之间的数据,或程序正在执行中，请稍后操作",
            'locationNow': controlMotor.photoelectricSensor.locationCount
        }
        return json.dumps(templateData)
    controlMotor.photoelectricSensor.timeFlag = time.time()
    controlMotor.photoelectricSensor.executing = True
    templateData = {
        'message': "程序已启动",
        'locationNow': controlMotor.photoelectricSensor.specifiedLocation(int(location))
    }
    return json.dumps(templateData)


@app.route("/init")
def init():
    # controlMotor.photoelectricSensor.executing = True
    # timeFlagLocal = time.time()
    # timeoutLocal = 0
    # controlMotor.relayLeft.setHigh()
    # controlMotor.relayRight.setHigh()
    # controlMotor.photoelectricSensor.uninstall()
    # controlMotor.relayLeft.setLow()
    # while GPIO.input(controlMotor.reedSwitch.reedSwitchPin) == GPIO.HIGH and timeoutLocal < 5000:
    #     timeoutLocal = time.time() - timeFlagLocal
    #     pass
    # controlMotor.relayLeft.setHigh()
    # controlMotor.photoelectricSensor.install()

    controlMotor.init_motor()
    templateData = {
        'message': "设备初始化已经执行完毕"
    }

    return json.dumps(templateData)


@app.route("/set/location/<location>")
def setLocation(location):
    if controlMotor.photoelectricSensor.executing:
        return "设备正在执行任务，稍后再试！"
    else:
        if int(location) > 7 or int(location) < 0:
            return "位置指定只能选择0-7之间！"
        controlMotor.photoelectricSensor.locationCount = int(location)
        controlMotor.photoelectricSensor.locationNO = -1
        return "设置成功，当前设置位置为：" + str(location)


@app.route("/current/position")
def currentPosition():
    return str(controlMotor.photoelectricSensor.locationCount)


def releaseResources():
    controlMotor.relayStop()
    print("卸载光电传感器")
    GPIO.remove_event_detect(controlMotor.photoelectricSensorPin)
    print("设备归位中。。。")
    timeFlag = time.time()
    timeout = 0
    controlMotor.relayLeft.setLow()
    while (GPIO.input(controlMotor.reedSwitchPin) != GPIO.LOW) and timeout < 5000:
        timeout = time.time() - timeFlag
        # print timeout
        pass
    print("主程序清理")
    GPIO.cleanup()


@app.route("/shutdown")
def shutdown():
    releaseResources()
    os.system("sudo shutdown -h now")


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
        # app.run(debug=False, threaded=True)
    finally:
        releaseResources()
