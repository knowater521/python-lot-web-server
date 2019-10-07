# coding=utf-8
from RPi import GPIO


class Relay(object):
    def __init__(self, relayPin):
        print "继电器：", relayPin, "准备..."
        self.relayPin = relayPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relayPin, GPIO.OUT)
        GPIO.output(relayPin, GPIO.HIGH)

    def setLow(self):
        GPIO.output(self.relayPin, GPIO.LOW)

    def setHigh(self):
        GPIO.output(self.relayPin, GPIO.HIGH)
