import pigpio
import constants
import chewnumber
import threaded_pin
import initialisation

# Function definitions

def fpgaShouldRead():
    initialisation.pi.write(constants.MOSI_PIN, 0)

def fpgaShouldWrite():
    initialisation.pi.write(constants.MOSI_PIN, 1)
    
def activateSlave():
    initialisation.pi.write(constants.SLAVESELECT_PIN, 0)

def deactivateSlave():
    initialisation.pi.write(constants.SLAVESELECT_PIN, 1)


def writeBit(cycles,data):
    # TODO switch to threads instead of writing/reading sequentially
    #global pi

    i=0
    for currentTuple in constants.WRITE_PINS:
        currentPin=currentTuple[1]
        key=currentTuple[0]
        # global debug
        # if debug:
        #     print("writing to current pin",currentPin,key,"data",data[i],"currently at bit",cycles,"which is",data[i][cycles])
        currentBit=data[i][cycles]
        initialisation.pi.write(currentPin, int(currentBit))
        i+=1

def readBit():
    #global pi
    # TODO switch to threads instead of writing/reading sequentially
    bitList=[]
    for currentTuple in constants.READ_PINS:
        currentPin=currentTuple[1]
        key=currentTuple[0]
        currentData=initialisation.pi.read(currentPin)
        # global debug
        # if debug:
        #     print("reading current pin", currentPin, key, "data", currentData)

        bitList.append(currentData)

    return bitList

def readData():
    receivedData = []
    currentCycle = 0
    previousClock = initialisation.pi.read(constants.CLOCK_PIN)
    decreasing=[7,6,5,4,3,2,1,0]
	
    fpgaShouldWrite()
    activateSlave()  
    while len(receivedData)<8:
        currentClock = initialisation.pi.read(constants.CLOCK_PIN)
        if (currentClock != previousClock and currentClock == 1):
            if currentCycle == 0:
                readBank()
            if (currentCycle >= 1):
                receivedBits = readBank()
                receivedData.append(receivedBits)          

            currentCycle += 1
        previousClock = currentClock

    fpgaShouldRead()
    deactivateSlave()

    #read data from bank array
    for cycle in range(0,len(receivedData)):
        bankdata=receivedData[cycle]
        pin1=bankdata >> constants.READ_PINS[0][1] & 1
        pin2=bankdata >> constants.READ_PINS[1][1] & 1
        pin3=bankdata >> constants.READ_PINS[2][1] & 1
        pin4=bankdata >> constants.READ_PINS[3][1] & 1  
        receivedData[cycle]=[pin1,pin2,pin3,pin4]

        #todo remove this sstringwise conversion, it's slow
    buttondata = []
    for i in range(0, 8):
        buttondata.append(receivedData[i][3])

    formatdata3 = [0, 0, 0, 0]

    for j in range(2, 3):
        for i in range(1, 8):
	    #print(type("Format data:",formatdata3[j])
            #print(type("Received data:",receivedData[i][j])
	    #print(type("decreasing:", decreasing[i])
            formatdata3[j] |= receivedData[i][j] << decreasing[i]

    for num in range(2, 3):
        formatdata3[num] /= 8
        if receivedData[0][num] == 1:
            formatdata3[num] *= -1
    paddlespeed = formatdata3[2]

    # print("DATA WITH BINARY OPERATIONS:", formatdata2)
    # newxspeed=chewnumber.fixedPointToDec(''.join(formatdata[0]))
    # newyspeed=chewnumber.fixedPointToDec(''.join(formatdata[1]))
    # paddlespeed=chewnumber.fixedPointToDec(''.join(formatdata[2]))
    buttons = [False, False]
    # TODO remove this stringwise checking, maybe use gmpy popcount
    if buttondata[0:4].count(1) >= 3:
        buttons[0] = True
    if buttondata[4:8].count(1) >= 3:
        buttons[1] = True


    return (paddlespeed,buttons)

def connect(xspeed,yspeed,bounciness,isvertical):
    #TODO Make seperate function that only reads buttons and accelerometer


    # Converting data to binary
    print("sending data")
    print("xspeed,yspeed,bounciness,isvertical")
    print(xspeed,yspeed,bounciness,isvertical)

    data= [[],[],[]]

    datalist=[xspeed*8,yspeed*8,bounciness*8]
    decreasing = [7, 6, 5, 4, 3, 2, 1, 0]
    for value in range(0,3):
        for i in range(0,7):
            data[value].append(int(datalist[value]) >> i & 1)
        if datalist[value]<0:
            data[value]=[1]+data[value]
        else:
            data[value] = [0] + data[value]




    #TODO make this shit more efficient because string operations
    #data = list(map(chewnumber.decToFixedPoint, [xspeed, yspeed, bounciness]))
    #data[0]="00001111"
    #returndata = [[]]

    if isvertical:
        data.append([1]*8)
    else:
        data.append([0]*8)

    if constants.GPIO_SEND_RECEIVE_AT_ONCE: #send and receive at same time
        print(data)
        returndata=rwByteParallel(data)
    else:
        returndata=rwByteSequence(data)



    #todo remove this sstringwise conversion, it's slow


    buttondata=[]
    for i in range(0,8):
         buttondata.append(returndata[i][3])

    formatdata3=[0,0,0,0]

    for j in range (0,3):
        for i in range (1,8):
            formatdata3[j] |= returndata[i][j]<<decreasing[i]

    for num in range(0,3):
        formatdata3[num] /=8
        if returndata[0][num]==1:
            formatdata3[num]*=-1

    newxspeed = formatdata3[0]
    newyspeed = formatdata3[1]
    paddlespeed = formatdata3[2]

    # print("DATA WITH BINARY OPERATIONS:", formatdata2)
    # newxspeed=chewnumber.fixedPointToDec(''.join(formatdata[0]))
    # newyspeed=chewnumber.fixedPointToDec(''.join(formatdata[1]))
    # paddlespeed=chewnumber.fixedPointToDec(''.join(formatdata[2]))
    buttons=[False,False]
    #TODO remove this stringwise checking, maybe use gmpy popcount
    if buttondata[0:4].count(1)>=3:
        buttons[0]=True
    if buttondata[4:8].count(1)>=3:
        buttons[1]=True

    print("received data")
    print(returndata)
    print("(newxspeed,newyspeed,paddlespeed,buttons)")
    print(newxspeed,newyspeed,paddlespeed,buttons)
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
#                 fpgaShouldRead()
#             if currentCycle <= 7:
#                 writeBit(currentCycle, data)
#             if currentCycle >= 1:
#                 receivedBits = readBit()
#                 receivedData.append(receivedBits)
#             currentCycle += 1
#
#         previousClock = currentClock
#
#     fpgaShouldWrite()
#     return receivedData

def writeBank(on,off):
    initialisation.pi.clear_bank_1(off)
    initialisation.pi.set_bank_1(on)

def readBank():
    return initialisation.pi.read_bank_1()




def rwByteSequence(data):
    data=data[:]
    receivedData = []
    currentCycle = 0
    previousClock = initialisation.pi.read(constants.CLOCK_PIN)

    #get bank array ready
    on_writeBankData=[]
    off_writeBankData=[]
    for cycles in range(0,8):
        on_output=0
        off_output=0
        for i in range (0,4):
            bit=data[i][cycles]
            if bit=="1":
                on_output = on_output | 1<<constants.WRITE_PINS[i][1]
            else:
                off_output = off_output | 1<<constants.WRITE_PINS[i][1]        
        on_writeBankData.append(on_output)
        off_writeBankData.append(off_output)



    fpgaShouldRead()
    activateSlave()  
    while True:
        currentClock = initialisation.pi.read(constants.CLOCK_PIN)
        if (currentClock != previousClock and currentClock == 1 and currentCycle <= 10):
            # TODO check if sleeps are needed to allow for game rendering, higher fps
            #if currentCycle == 0:
                #fpgaShouldRead()
            if currentCycle <= 1:
                writeBank(0,0)                
            if currentCycle >= 2 and currentCycle <= 9:              
                #data = ["010000000", "000010011", "000001010", "000000000"]




                #writeBit(currentCycle-2, data)
                writeBank(on_writeBankData[currentCycle-2],off_writeBankData[currentCycle-2])





            if currentCycle == 10:
                deactivateSlave()            
            #elif currentCycle >= 11 and currentCycle <= 19:
                #fpgaShouldWrite() #actually receiving
               # activateSlave()
               # receivedBits = threaded_pin.readBit()

               # if currentCycle >= 12:
                #    receivedData.append(receivedBits)
            #elif currentCycle>=20:
                #fpgaShouldRead()
                #deactivateSlave()
            currentCycle += 1
        elif (currentClock != previousClock and currentClock == 0 and currentCycle >= 11):
            if currentCycle == 11:
                activateSlave()
                fpgaShouldWrite()
                readBank()
            if (currentCycle >= 12 and currentCycle<=19):
                receivedBits = readBank()
                receivedData.append(receivedBits)
            if currentCycle ==20:
                readBank()
                deactivateSlave()
                break
            #TODO maybe add a cycle 21
                

            currentCycle += 1
        previousClock = currentClock




    #read data from bank array
    for cycle in range(0,len(receivedData)):
        bankdata=receivedData[cycle]
        pin1=bankdata >> constants.READ_PINS[0][1] & 1
        pin2=bankdata >> constants.READ_PINS[1][1] & 1
        pin3=bankdata >> constants.READ_PINS[2][1] & 1
        pin4=bankdata >> constants.READ_PINS[3][1] & 1  
        receivedData[cycle]=[pin1,pin2,pin3,pin4]

    return receivedData


    
def closeConnection():
    #global pi
    initialisation.pi.stop()

def main():
    #global debug
    debug=True
    initialisation.initConnection()
    # WRITE THE VALUES YOU WANT TO SEND HERE
    xspeed = -3
    yspeed = 2
    bounciness = 3
    isvertical = False

    print("(xspeed,yspeed,bounciness,isvertical)")
    print(xspeed,yspeed,bounciness,isvertical)
    returnval=connect(xspeed,yspeed,bounciness,isvertical)


 

    closeConnection()

if __name__ == "__main__":
    main()
    

#banks should work now


    
    
