#Is slower and works worse than just polling the clock

import constants
# Initialize pigpio daemon
from subprocess import call
call(["sudo", "pigpiod"])

#Importing libraries
import psutil, os
import pigpio
import chewnumber
from threading import Event
global exit

#Setting variables
exit = Event()
p = psutil.Process(os.getpid())
p.nice(-19)
pi = pigpio.pi('Dragon47')
n=3




#pi.hardware_clock(4,4689)
pi.set_PWM_frequency(4, constants.CLOCKSPEED)
pi.set_PWM_dutycycle(4, constants.DUTYCYCLE)

pi.write(10, 1)


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
global totalattempts
totalattempts=10


for i in range(0,3):
    send_value_bin[i]=chewnumber.decToInt(send_value[i])



def clockcycler(gpio, level, tick):

    #TODO call functions from here
    #TODO use less global variables,transfer to class
    global res
    global pin
    global send_value_bin
    global cb2
    global running
    global totalattempts
    print("cycle")
    #tally=cb2.tally()
    cycle=tally%9

    if cycle==0:
        pi.write(10, 0)

    pinout=pi.read(pin)
    res.append(pinout)

    if (cycle == 8):
        pi.write(10, 1)
        print(res)

        res=[]
        if tally/9>=totalattempts-1:
            print("DONE")

            cb1.cancel()
            running=False
            exit.set()




global pin
global attempt
pin=16

global attempt
attempt=0
global running
running=True



cb1 = pi.callback(11, pigpio.RISING_EDGE, clockcycler) #this should go outside  while loop, why is it so slow?

#global cb2
#cb2 = pi.callback(4, pigpio.RISING_EDGE)

#TODO fix this
while not exit.is_set():
   try:
      exit.wait(60)
   except InterruptExecution:
      break

print("done, tidying up")
pi.stop()
exit.clear()
    #select += 1
    #sleep(0.1)



    
    
