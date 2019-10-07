# -*- coding: utf-8 -*
"""
滑轨控制
"""
import time

import RPi.GPIO as GPIO
from flask import Flask, json

from controlMotor import ControlMotor

app = Flask(__name__)

controlMotor = ControlMotor(17, 16, 13, 12, 20, 18, 19,5,7)


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
    print "当前运行方向", direction, "当前位置", locationCount
    changePin = int(changePin)
    if action == "on".lower():
        if controlMotor.relayLeft.relayPin != changePin:
            controlMotor.relayLeft.setHigh()
        if controlMotor.relayRight.relayPin != changePin:
            controlMotor.relayRight.setHigh()
        if changePin == 18:
            if locationCount > 1:
                controlMotor.relayLeft.setLow()
                controlMotor.reedSwitch.direction = "left"
                print "左转继电器开启"
            else:
                print "到达1号位置，设置方向为向右"
                controlMotor.reedSwitch.direction = "right"
                return "off"
        else:
            if locationCount < 7:
                controlMotor.relayRight.setLow()
                controlMotor.reedSwitch.direction = "right"
                print "右转继电器开启"
            else:
                print "到达7号位置，设置方向为向左"
                controlMotor.reedSwitch.direction = "left"
                return "off"
        return "on"
    if action == "off":
        controlMotor.relayRight.setHigh()
        controlMotor.relayLeft.setHigh()
        return "off"


@app.route("/relay/<changePin>/<action>")
def relayControl(changePin, action):

    templateData = {
        'relayPins': changePin,
        'relayMessage': setRelay(changePin, action)
    }
    return json.dumps(templateData)


@app.route("/specified/<location>")
def specifiedLocation(location):
    if int(location) > 7 or int(location) < 1:
        templateData = {
            'message': "只能选择1-7之间的数据",
            'locationNow': controlMotor.photoelectricSensor.locationCount
        }
        return json.dumps(templateData)
    templateData = {
        'message': "程序已启动",
        'locationNow': controlMotor.photoelectricSensor.specifiedLocation(int(location))
    }
    return json.dumps(templateData)


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
    finally:
        print "卸载光电传感器"
        GPIO.remove_event_detect(controlMotor.photoelectricSensorPin)
        print "设备归位中。。。"
        timeFlag = time.time()
        controlMotor.relayLeft.setLow()
        while (GPIO.input(controlMotor.reedSwitchPin) != GPIO.LOW) or (time.time() - timeFlag < 60):
            pass
        print "主程序清理"
        GPIO.cleanup()
