from time import sleep
#import RPi.GPIO as GPIO
import psutil, os
import pigpio

p = psutil.Process(os.getpid())
p.nice(-19)

pi = pigpio.pi('Dragon47')



pi.set_PWM_frequency(11, 1000)
pi.set_PWM_dutycycle(11,127)


pi.write(10, 1)






#WRITE THE VALUE YOU WANT TO SEND HERE
send_value[0]=9
send_value[1]=8
send_value[2]=7











for i in range(0,3):
    send_value_bin[i]=bin(send_value[i])[2:]

    if len(send_value_bin[i]) > 8:
        print("overflow")

    if len(send_value_bin[i])<8:
        diff[i]=8-len(send_value_bin[i])
        zerolist[i]=(diff[i])*['0']
        zerostring[i]=''.join(zerolist[i])
        send_value_bin[i]=zerostring[i]+send_value_bin[i]

def readinfo(pin,i):
    res = []
    cycles = 0
    #TODO find out if there is a neater way to detect clock than read pin 11

    clock_value_previous = pi.read(11) #GPIO.input(23)
    


    print(send_value_bin)
    while True:
        clock_value_now = pi.read(11) #GPIO.input(23)
        if (clock_value_now != clock_value_previous and clock_value_now == 1):


            for i in range(0,3)
            if cycles <=7:
                writecycle=send_value_bin[i][cycles]
                pi.write(23+i, int(writecycle))
            else:


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
    

for i in range(60):
    print(readinfo(16))

    #select += 1
    #sleep(0.1)
print("DONE")
pi.write(25,0)
pi.stop()


    
    
