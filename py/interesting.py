from time import sleep
import psutil, os
import pigpio
import chewnumber
from subprocess import call

call(["sudo", "pigpiod"])
pi = pigpio.pi('Dragon47')

def initialise(clock_frequency):
    p = psutil.Process(os.getpid())
    p.nice(-19)
    pi.set_PWM_frequency(11, clock_frequency)
    pi.set_PWM_dutycycle(11,128)
    mosiSignal(1)
    print("Clock frequency set to:", clock_frequency, "Hz")
    print("Initalised... starting to run")
    
def mosiSignal(signal):
    pi.write(10, signal)
    
def clockValue():
    return pi.read(11)
    
GPIO = [17, 18, 27, 22, 23, 24, 25, 27, 26]

""" This now reads at all the pins (in "GPIO" array) and discards
the first bit (from a sequence of 9)for each pin """
def readinfo():
    res = [[]]
    cycles = 0
    clock_value_previous = clockValue()
    while True:
        clock_value_now = clockValue()
        if (clock_value_now != clock_value_previous and clock_value_now == 1):
            mosiSignal(0)
            for i in range(9):
                res[i].append(pi.read(GPIO[i]))
            #cycles += 1
        if (len(res[0]) == 9):
            mosiSignal(1)
            for i in range(9):
                res[i] = res[i][1:]
            break
        clock_value_previous = clock_value_now
    return res

initialise(1000)
print("DONE")
pi.stop()


    
    

