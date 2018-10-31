from subprocess import call

call(["sudo", "pigpiod"])

from time import sleep

#import RPi.GPIO as GPIO
import psutil, os
import pigpio
import chewnumber

p = psutil.Process(os.getpid())
p.nice(-19)

pi = pigpio.pi('Dragon47')



pi.set_PWM_frequency(11, 1000)
pi.set_PWM_dutycycle(11,100)


pi.write(10, 1)
n=3

global send_value_bin
send_value=[0]*n
send_value_bin=[0]*n
zerostring=[0]*n
diff=[0]*n
zerolist=[0]*n




#WRITE THE VALUE YOU WANT TO SEND HERE
send_value[0]=0x13
send_value[1]=0x37
send_value[2]=0x69


global cycles
cycles=0
global res
res=[]





for i in range(0,3):
    send_value_bin[i]=chewnumber.decToInt(send_value[i])


def clockcycler():
    #TODO call functions from here
    #TODO use less global variables
    #print("Cycle")
    global res
    global cycles
    global pin
    global send_value_bin
    global cb1
    global attempt
    global running
    for i in range(0, 3):
        if cycles <= 7:
            writecycle = send_value_bin[i][cycles]
            pi.write(23 + i, int(writecycle))
            #print("wrote to pin",23+i)
        # else:
        #  pi.write(23+i, 0)

    pi.write(10, 0)
    pinout=pi.read(pin)
    res.append(pinout)
    #print("read from pin",pin,"value is",pinout)
    #print(len(res))
    if (len(res) == 9):
        print("res is len 9")
        print(res)
        attempt+=1
        pi.write(10, 1)
        print(attempt)
        if attempt >= 0:
            # print(returnval)

            returnvaldec = chewnumber.intToDec(''.join(list(map(str, res[1:]))))
            # print(returnvaldec)

            print(res, '=', returnvaldec)
        res=[]
        cycles=0
        if attempt>=50:
            cb1.cancel()
            print("DONE")
            pi.write(25, 0)

            pi.stop()
            running=False


    cycles += 1

def readinfo():
    global res
    global cycles

    cycles = 0
    res=[]
    # TODO find out if there is a neater way to detect clock than read pin 11
    # TODO use threading to send data



    


global pin
global attempt
pin=16

global attempt
attempt=0
global running
running=True
global cb1




#TODO fix this
while running==True:
    cb1 = pi.callback(11, pigpio.RISING_EDGE, clockcycler()) #this should go outside  while loop, why is it so slow?
    #why does this not work outside while loop?
    pass


    #select += 1
    #sleep(0.1)



    
    
