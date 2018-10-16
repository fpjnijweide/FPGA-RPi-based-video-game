#!/usr/bin/env python3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
clock = GPIO.PWM(3, 0)          # just to have clock as a global variable. this will make the clock unusable

def setUpPins():
    GPIO.setup(2, GPIO.OUT)     # Clock
    clock = GPIO.PWM(2, 5000)
    clock.start(50)             # start the clock with duty cycle = 50% (50% of time being 1, 50% being 0)
    GPIO.setup(3, GPIO.OUT)     # Send signal (0->receiving from FPGA, 1->sending data for calculation)

    return

def sendData():
    return

def stopConnection():
    clock.stop()                # stop the clock
    GPIO.cleanup()              # stop any operation on the pins




