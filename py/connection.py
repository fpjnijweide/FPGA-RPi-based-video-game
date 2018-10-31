import psutil, os
import pigpio
import constants
import chewnumber
from subprocess import call

# Function definitions

def readyToReceive():
    pi.write(constants.MOSI_PIN, 0)

def notReadyToReceive():
    pi.write(constants.MOSI_PIN, 1)

def writeBit(cycles,data):
    # TODO switch to threads instead of writing/reading sequentially
    i=0
    for key,currentPin in constants.WRITE_PINS.items():

        currentBit=data[i][cycles]
        pi.write(currentPin, int(currentBit))
        i+=1

def readBit(readPin):
    # TODO switch to threads instead of writing/reading sequentially
    bitList=[]
    for key, currentPin in constants.READ_PINS.items():
        bitList.append(pi.read(currentPin))
    return bitList

def connect(xspeed,yspeed,bounciness,isvertical):
    # Converting data to binary
    data = list(map(chewnumber.decToFixedPoint, [xspeed, yspeed, bounciness, isvertical]))

    if constants.GPIO_SEND_RECEIVE_AT_ONCE: #send and receive at same time
        rwByteParallel(data)
    else:
        rwByteSequence(data)

    #TODO Print sent and received data (xspeed,yspeed etc) in readable formats


def rwByteParallel(data):
    receivedData = []
    currentCycle = 0
    previousClock = pi.read(constants.CLOCK_PIN)

    while len(receivedData) < 9:
        currentClock = pi.read(constants.CLOCK_PIN)
        if (currentClock != previousClock and currentClock == 1):
            # TODO check if sleeps are needed to allow for game rendering, higher fps
            if currentCycle == 0:
                readyToReceive()
            if currentCycle <= 7:
                writeBit(currentCycle, data)
            if currentCycle >= 1:
                receivedBits = readBit()
                receivedData.append(receivedBits)
            currentCycle += 1

        previousClock = currentClock

    notReadyToReceive()
    return receivedData

def rwByteSequence(data):
    receivedData = []
    currentCycle = 0
    previousClock = pi.read(constants.CLOCK_PIN)

    while len(receivedData)<9:
        currentClock = pi.read(constants.CLOCK_PIN)
        if (currentClock != previousClock and currentClock == 1):
            # TODO check if sleeps are needed to allow for game rendering, higher fps
            if currentCycle == 0:
                readyToReceive()
            if currentCycle <= 7:
                writeBit(currentCycle, data)
            if currentCycle ==9:
                notReadyToReceive()
            if currentCycle==10:
                readyToReceive()
            if currentCycle >= 9+1 and currentCycle <= 9+8
                receivedBits = readBit()
                receivedData.append(receivedBits)
            currentCycle += 1

        previousClock = currentClock

    notReadyToReceive()
    return receivedData

def initConnection():
    #START DAEMON
    call(["sudo", "pigpiod"])

    # STARTING PROCESS, SET PRIORITY
    p = psutil.Process(os.getpid())  # make process high priority
    p.nice(-19)
    pi = pigpio.pi('Dragon47')

    # Starting clock
    pi.set_PWM_frequency(constants.CLOCK_PIN, constants.CLOCKSPEED)
    pi.set_PWM_dutycycle(constants.CLOCK_PIN, constants.DUTYCYCLE)

    pi.write(constants.MOSI_PIN, 1)  # make sure no data is sent yet

def main():
    initConnection()
    # WRITE THE VALUES YOU WANT TO SEND HERE
    xspeed = 2
    yspeed = 3
    bounciness = 1.125
    isvertical = True

    for i in range(60):
        returnval=connect(xspeed,yspeed,bounciness,isvertical)
        print(returnval)
    print("DONE")
    pi.stop()

if __name__ == "__main__":
    main()



    
    
