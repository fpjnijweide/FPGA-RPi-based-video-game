import psutil, os
import pigpio
import constants
import chewnumber

#Start Daemon
from subprocess import call
call(["sudo", "pigpiod"])

#STARTING PROCESS
p = psutil.Process(os.getpid()) #make process high priority
p.nice(-19)
pi = pigpio.pi('Dragon47')

#Starting clock
pi.set_PWM_frequency(constants.CLOCK_PIN, constants.CLOCKSPEED)
pi.set_PWM_dutycycle(constants.CLOCK_PIN, constants.DUTYCYCLE)

pi.write(constants.MOSI_PIN, 1) #make sure no data is sent yet

# WRITE THE VALUES YOU WANT TO SEND HERE
xspeed=2
yspeed=3
bounciness=1.125
isvertical=True

#Converting data to binary
data=list(map(chewnumber.decToFixedPoint,[xspeed,yspeed,bounciness,isvertical]))


#########################################

# Function definitions

def readyToReceive():
    pi.write(constants.MOSI_PIN, 0)

def notReadyToReceive():
    pi.write(constants.MOSI_PIN, 1)

def writeCycle(cycles,data):
    i=0
    for key,currentPin in constants.WRITE_PINS.items():
        if cycles <=7:
            currentBit=data[i][cycles]
            pi.write(currentPin, int(currentBit))
        i+=1

def rwbyte(pin):
    res = []
    cycles = 0
    #TODO switch to threads instead of writing/reading sequentially

    clock_value_previous = pi.read(11)

    while True:
        clock_value_now = pi.read(11)
        if (clock_value_now != clock_value_previous and clock_value_now == 1):
            if cycles==0:
                readyToReceive()

            writeCycle(cycles,data)

            res.append(pi.read(pin))
            cycles += 1
            
            if (len(res) == 9):
                notReadyToReceive()
                break
        clock_value_previous = clock_value_now
    return res
    

def main():
    for i in range(60):
        print(rwbyte(16))

        # select += 1
        # sleep(0.1)
    print("DONE")
    pi.write(25, 0)
    pi.stop()

if __name__ == "__main__":
    main()



    
    
