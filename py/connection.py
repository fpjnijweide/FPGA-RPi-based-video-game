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
    for currentTuple in list(constants.WRITE_PINS.items()):
        currentPin=currentTuple[1]
        key=currentTuple[0]
        print("writing to current pin",currentPin,key,"data",data[i],"currently at bit",cycles,"which is",data[i][cycles])
        currentBit=data[i][cycles]
        pi.write(currentPin, int(currentBit))
        i+=1

def readBit():
    # TODO switch to threads instead of writing/reading sequentially
    bitList=[]
    for currentTuple in list(constants.READ_PINS.items()):
        currentPin=currentTuple[1]
        key=currentTuple[0]
        currentData=pi.read(currentPin)
        print("writing to current pin", currentPin, key, "data", currentData)
        bitList.append(currentData)

    return bitList

def connect(xspeed,yspeed,bounciness,isvertical):
    # Converting data to binary
    data = list(map(chewnumber.decToFixedPoint, [xspeed, yspeed, bounciness]))

    if isvertical:
        data.append("11111111")
    else:
        data.append("00000000")

    if constants.GPIO_SEND_RECEIVE_AT_ONCE: #send and receive at same time
        return rwByteParallel(data)
    else:
        print("running rwbytesequence")
        print("data")
        print(data)
        return rwByteSequence(data)

    #TODO Print sent and received data (xspeed,yspeed etc) in readable formats


def rwByteParallel(data):
    data=data[:]
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
    data=data[:]
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
            if currentCycle >= 9+1 and currentCycle <= 9+8:
                receivedBits = readBit()
                receivedData.append(receivedBits)
            currentCycle += 1

        previousClock = currentClock

    notReadyToReceive()
    return receivedData

def initConnection():
    global pi
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
    xspeed = 14
    yspeed = 0
    bounciness = 1.125
    isvertical = True

    for i in range(60):
        returnval=connect(xspeed,yspeed,bounciness,isvertical)
        print(returnval)
    print("DONE")
    pi.stop()

if __name__ == "__main__":
    main()



    
    
