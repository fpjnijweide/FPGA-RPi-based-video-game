from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

eureka = False
nrOfZeros = 0
nrOfOnes = 0
testing_pins = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40]
for i in range(len(testing_pins)):
    GPIO.setup(testing_pins[i], GPIO.IN)

    
while 1:    
        for i in range(len(testing_pins)):
            whichPin = testing_pins[i]
            print("Value of pin",str(whichPin),":",GPIO.input(whichPin))
            if GPIO.input(whichPin) == 1:
                eureka = True
                nrOfOnes += 1
            else:
                nrOfZeros += 1
        
        if eureka:
            print("~~~~~~~~~~~~~~~~~~~~")
            print("Number of read pins:", len(testing_pins))
            print("Number of ones:", nrOfOnes)
            print("Number of zeros:", nrOfZeros)
            break
        sleep(0.1)