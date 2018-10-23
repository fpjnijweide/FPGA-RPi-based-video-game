#!/usr/bin/env python3
import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

cycles = 5000
frequency = 5000
sleepdelay = 1/frequency
SPIpins = [10,9,11,8]
# data = [5,6,13,19,26]
dataPins = [26,16,20,21]
running = True

def threaded_function():
    while running:

GPIO.setmode(GPIO.BCM)


def setUp():
    thread = Thread(target=threaded_function)
    thread.start()
    thread.join()
    return

if __name__ == '__main__':
    main()

def main():
    setUp()
    for x in dataPins:
        print(x)
        GPIO.setup(x, GPIO.OUT)
    while running:
        sendData()
    stopConnection()

def sendData():
    return

def stopConnection():              # stop the clock
    GPIO.cleanup()              # stop any operation on the pins
