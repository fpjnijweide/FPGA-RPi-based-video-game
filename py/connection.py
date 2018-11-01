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

def writeBank(cycles,data):
    # TODO check performance
    # TODO check if result is even same
    xspeedbit=data[0][cycles] #xspeed
    yspeedbit=data[1][cycles]#yspeed
    bouncinessbit=data[2][cycles]#bouciness
    is_verticalbit=data[3][cycles]#isvertical


    xspeedpin=constants.WRITE_PINS[0][2]
    yspeedpin = constants.WRITE_PINS[1][2]
    bouncinesspin = constants.WRITE_PINS[0][2]
    is_verticalpin=constants.WRITE_PINS[0][2]

    bitstring=['0']*32
    bitstring[xspeedpin]=str(xspeedbit)
    bitstring[yspeedpin]=str(yspeedbit)
    bitstring[bouncinesspin]=str(bouncinessbit)
    bitstring[is_verticalpin]=str(is_verticalbit)

    pi.set_bank_1(int(''.join(bitstring),2))

def readBank():
    # TODO check performance
    # TODO check if result is even same
    bankdata=bin(pi.read_bank_1())[2:]
    pin1=constants.READ_PINS[0][2]
    pin2=constants.READ_PINS[1][2]
    pin3=constants.READ_PINS[2][2]
    pin4=constants.READ_PINS[3][2]

    return list(map(int, [bankdata[pin1],bankdata[pin2],bankdata[pin3],bankdata[pin4]]))

def writeBit(cycles,data):
    # TODO switch to threads instead of writing/reading sequentially


    i=0
    for currentTuple in constants.WRITE_PINS:
        currentPin=currentTuple[1]
        key=currentTuple[0]
        global debug
        if debug:
            print("writing to current pin",currentPin,key,"data",data[i],"currently at bit",cycles,"which is",data[i][cycles])
        currentBit=data[i][cycles]
        pi.write(currentPin, int(currentBit))
        i+=1

def readBit():

    # TODO switch to threads instead of writing/reading sequentially
    bitList=[]
    for currentTuple in constants.READ_PINS:
        currentPin=currentTuple[1]
        key=currentTuple[0]
        currentData=pi.read(currentPin)

        global debug
        if debug:
            print("reading current pin", currentPin, key, "data", currentData)
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
        print("read/wriitng in sequence")
        print("sending data")
        print(data)
        returndata=rwByteParallel(data)
    else:
        print("read/wriitng in sequence")
        print("sending data")
        print(data)
        returndata=rwByteSequence(data)

    print("received data")
    print(returndata)

    #TODO print in readable formats
    # print("formatted data")
    # xspeed1=[]
    #
    # for i in range(0,8):
    #     xspeed

    newxspeed=0
    newyspeed=0
    paddlespeed=0
    buttons=0
    return (newxspeed,newyspeed,paddlespeed,buttons)



# def rwByteParallel(data):
#     data=data[:]
#     receivedData = []
#     currentCycle = 0
#     previousClock = pi.read(constants.CLOCK_PIN)
#
#     while len(receivedData) < 9:
#         currentClock = pi.read(constants.CLOCK_PIN)
#         if (currentClock != previousClock and currentClock == 1):
#             # TODO check if sleeps are needed to allow for game rendering, higher fps
#             if currentCycle == 0:
#                 readyToReceive()
#             if currentCycle <= 7:
#                 writeBit(currentCycle, data)
#             if currentCycle >= 1:
#                 receivedBits = readBit()
#                 receivedData.append(receivedBits)
#             currentCycle += 1
#
#         previousClock = currentClock
#
#     notReadyToReceive()
#     return receivedData

def rwByteSequence(data):
    data=data[:]
    receivedData = []
    currentCycle = 0
    previousClock = pi.read(constants.CLOCK_PIN)

    while len(receivedData)<8:
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
            if currentCycle >= 10 and currentCycle <= 18:
                receivedBits = readBit()
                if currentCycle >= 11:
                    receivedData.append(receivedBits)
            currentCycle += 1

        previousClock = currentClock

    notReadyToReceive()
    return receivedData

def initConnection():
    global pi
    global debug
    debug=True
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
    xspeed =  -8.875
    yspeed = -4.875
    bounciness = 0.875
    isvertical = False

    returnval=connect(xspeed,yspeed,bounciness,isvertical)

    print("DONE")
    pi.stop()

if __name__ == "__main__":
    main()



    
    
