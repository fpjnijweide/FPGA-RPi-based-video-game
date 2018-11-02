import threading
import constants
import initialisation


class threadPin (threading.Thread):
    global pi
    def __init__(self, name, pin):
        threading.Thread.__init__(self)
        self.name = name
        self.pin = pin
    def write(self, bit):
        print("Writing the bit", bit, "to pin", self.pin)
        initialisation.pi.write(self.pin, int(bit))
    def read(self):
        print("Reading the bit", initialisation.pi.read(self.pin), "on pin", self.pin)
        return initialisation.pi.read(self.pin)

for i in range(4):
    name_R = constants.READ_PINS[i][0]
    pin_R = constants.READ_PINS[i][1]
    name_W = constants.WRITE_PINS[i][0]
    pin_W = constants.WRITE_PINS[i][1]
    if (i == 0):
        xSpeed_R = threadPin(name_R, pin_R)
        xSpeed_W = threadPin(name_W, pin_W)
    elif (i == 1):
        ySpeed_R = threadPin(name_R, pin_R)
        ySpeed_W = threadPin(name_W, pin_W)
    elif (i == 2):
        paddleSpeed = threadPin(name_R, pin_R)
        bounciness = threadPin(name_W, pin_W)
    elif (i == 3):
        buttons = threadPin(name_R, pin_R)
        isVertical = threadPin(name_W, pin_W)


             

def writeBit(cycles,data):
    global pi
    print("currently at cycle nr", cycles)
    print(data[0][cycles])
    xSpeed_W.write(data[0][cycles])
    ySpeed_W.write(data[1][cycles])
    bounciness.write(data[2][cycles])
    isVertical.write(data[3][cycles])
    
def readBit():
    global pi
    bitList=[]
    bitList.append(xSpeed_R.read())
    bitList.append(ySpeed_R.read())
    bitList.append(paddleSpeed.read())
    bitList.append(buttons.read())
    print(bitList)
    return bitList
