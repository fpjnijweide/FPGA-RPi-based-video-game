from time import sleep
import psutil, os
import pigpio

def initialise():
    p = psutil.Process(os.getpid())
    p.nice(-19)
    pi = pigpio.pi('Dragon47')
    pi.set_PWM_frequency(11, 1000)
    pi.set_PWM_dutycycle(11,128)

pi.write(10, 1)

#WRITE THE VALUE YOU WANT TO SEND HERE
send_value=9

send_value_bin=bin(send_value)[2:]

if len(send_value_bin) > 8:
    print("overflow")

if len(send_value_bin)<8:
    diff=8-len(send_value_bin)
    zerolist=diff*['0']
    zerostring=''.join(zerolist)
    send_value_bin=zerostring+send_value_bin

def readinfo(pin):
    res = []
    cycles = 0
    #TODO find out if there is a neater way to detect clock than read pin 11
    clock_value_previous = pi.read(11)
    while True:
        clock_value_now = pi.read(11) #GPIO.input(23)
        if (clock_value_now != clock_value_previous and clock_value_now == 1):
            
            if cycles <=7:
                writecycle=send_value_bin[cycles]
                pi.write(25, int(writecycle))

            pi.write(10, 0)
            res.append(pi.read(pin))
            #pi.write(24, 0)
            #pi.write(23, 0)

            cycles += 1
        if (len(res) == 9):
            pi.write(10, 1)
            break
        clock_value_previous = clock_value_now
    return res

initialise()
for i in range(60):
    print(readinfo(16))
print("DONE")
pi.write(25,0)
pi.stop()


    
    
