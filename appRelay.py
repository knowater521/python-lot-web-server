# -*- coding: utf-8 -*
"""
Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson
Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com
"""
import time

import RPi.GPIO as GPIO
from flask import Flask, json

from button import Button
from controlMotor import ControlMotor
from motor import Motor
from photoelectricSensor import PhotoelectricSensor
from reedSwitch import ReedSwitch
from relay import Relay

app = Flask(__name__)

controlMotor = ControlMotor(17, 16, 13, 12, 20, 18, 19,5,7)


@app.route("/")
def main():
    print "设置1号继电器开"
    setRelay(controlMotor.relayLeft.relayPin, "on")
    time.sleep(2)
    print "设置2号继电器开"
    setRelay(controlMotor.relayRight.relayPin, "on")
    time.sleep(2)

    print "设置1号继电器关"
    setRelay(controlMotor.relayLeft.relayPin, "off")
    time.sleep(2)
    print "设置2号继电器关"
    setRelay(controlMotor.relayRight.relayPin, "off")
    return "电机旋转10秒"


def setRelay(changePin, action):
    changePin = int(changePin)
    if action == "on".lower():
        if controlMotor.relayLeft.relayPin != changePin:
            controlMotor.relayLeft.setHigh()
        if controlMotor.relayRight.relayPin != changePin:
            controlMotor.relayRight.setHigh()
        GPIO.output(changePin, GPIO.LOW)
        if changePin == 18:
            controlMotor.reedSwitch.direction = "left"
            print "左转继电器开启"
        else:
            controlMotor.reedSwitch.direction = "right"
            print "右转继电器开启"
        return "on"
    if action == "off":
        GPIO.output(changePin, GPIO.HIGH)
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

    templateData = {
        'message': "程序已启动",
        'locationNow': controlMotor.photoelectricSensor.specifiedLocation(int(location))
    }
    return json.dumps(templateData)


if __name__ == "__main__":
    try:
        # app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
        app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
    finally:
        print "主程序清理"
        GPIO.cleanup()
