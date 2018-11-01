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
    global pi

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
    global pi
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

    formatdata=[[],[],[],[]]
    for i in range(0,8):
        formatdata[0].append(str(returndata[i][0]))
        formatdata[1].append(str(returndata[i][1]))
        formatdata[2].append(str(returndata[i][2]))
        formatdata[3].append(str(returndata[i][3]))

    newxspeed=chewnumber.fixedPointToDec(''.join(formatdata[0]))
    newyspeed=chewnumber.fixedPointToDec(''.join(formatdata[1]))
    paddlespeed=chewnumber.fixedPointToDec(''.join(formatdata[2]))
    buttondata=''.join(formatdata[3])

    if buttondata=="11111111":
        buttons=(True,True)
    elif buttondata=="11110000":
        buttons=(True,False)
    elif buttondata=="00001111":
        buttons=(False,True)
    elif buttondata=="00000000":
        buttons=(False,False)
    else:
        print("invalid button data")
        print(buttondata)
        buttons = (False, False)

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
            if currentCycle>=19:
                notReadyToReceive()
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

    # #Init pins
    # for readpin in constants.READ_PINS:
    #     pi.set_mode(readpin[1], pigpio.INPUT)
    #
    # for writepin in constants.WRITE_PINS:
    #     pi.set_mode(writepin[1], pigpio.OUTPUT)
    # pi.set_mode(constants.CLOCK_PIN, pigpio.OUTPUT)
    # pi.set_mode(constants.MOSI_PIN, pigpio.OUTPUT)


    # Starting clock
    pi.set_PWM_frequency(constants.CLOCK_PIN, constants.CLOCKSPEED)
    pi.set_PWM_dutycycle(constants.CLOCK_PIN, constants.DUTYCYCLE)

    pi.write(constants.MOSI_PIN, 1)  # make sure no data is sent yet

def closeConnection():
    global pi
    pi.stop()

def main():
    global debug
    debug=True
    initConnection()
    # WRITE THE VALUES YOU WANT TO SEND HERE
    xspeed = 0.125
    yspeed = 0.125
    bounciness = 0.125
    isvertical = True

    print("(xspeed,yspeed,bounciness,isvertical)")
    print(xspeed,yspeed,bounciness,isvertical)
    returnval=connect(xspeed,yspeed,bounciness,isvertical)


    print("DONE")
    print("(xspeed,yspeed,bounciness,isvertical)")
    print(xspeed,yspeed,bounciness,isvertical)
    print("(newxspeed,newyspeed,paddlespeed,buttons)")
    print(returnval)
    closeConnection()

if __name__ == "__main__":
    main()

#banks do not work


# def writeBank(cycles,data):
#     xspeedbit=data[0][cycles] #xspeed
#     yspeedbit=data[1][cycles]#yspeed
#     bouncinessbit=data[2][cycles]#bouciness
#     is_verticalbit=data[3][cycles]#isvertical
#
#
#     xspeedpin=constants.WRITE_PINS[0][2]
#     yspeedpin = constants.WRITE_PINS[1][2]
#     bouncinesspin = constants.WRITE_PINS[0][2]
#     is_verticalpin=constants.WRITE_PINS[0][2]
#
#     bitstring=['0']*32
#     bitstring[xspeedpin]=str(xspeedbit)
#     bitstring[yspeedpin]=str(yspeedbit)
#     bitstring[bouncinesspin]=str(bouncinessbit)
#     bitstring[is_verticalpin]=str(is_verticalbit)
#
#     pi.set_bank_1(int(''.join(bitstring),2))
#
# def readBank():
#     bankdata=bin(pi.read_bank_1())[2:]
#     pin1=constants.READ_PINS[0][2]
#     pin2=constants.READ_PINS[1][2]
#     pin3=constants.READ_PINS[2][2]
#     pin4=constants.READ_PINS[3][2]
#
#     return list(map(int, [bankdata[pin1],bankdata[pin2],bankdata[pin3],bankdata[pin4]]))



    
    
