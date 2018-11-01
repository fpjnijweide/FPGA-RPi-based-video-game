import psutil, os
import pigpio

p = psutil.Process(os.getpid())
p.nice(-19)

pi = pigpio.pi('Dragon47')
n=3


pi.set_PWM_frequency(11, 1000)
pi.set_PWM_dutycycle(11,127)


pi.write(10, 1)

send_value=n*[0]
data=n*[0]
diff=n*[0]
zerolist=n*[0]
zerostring=n*[0]


#WRITE THE VALUE YOU WANT TO SEND HERE
send_value[0]=0xAB
send_value[1]=0xCD
send_value[2]=0xEF



for i in range(0,3):
    data[i]=bin(send_value[i])[2:]

    if len(data[i]) > 8:
        print("overflow")

    if len(data[i])<8:
        diff[i]=8-len(data[i])
        zerolist[i]=(diff[i])*['0']
        zerostring[i]=''.join(zerolist[i])
        data[i]=zerostring[i]+data[i]

def writeCycle(cycles,data):
    for i in range(0,len(data)):
        if cycles <=7:
            writecycle=data[i][cycles]
            pi.write(23+i, int(writecycle))

def rwbyte(pin):
    res = []
    cycles = 0
    #TODO switch to threads instead of writing/reading sequentially

    clock_value_previous = pi.read(11)

    while True:
        clock_value_now = pi.read(11)
        if (clock_value_now != clock_value_previous and clock_value_now == 1):
            if cycles==0:
                pi.write(10, 0)

            writeCycle(cycles,data)

            res.append(pi.read(pin))
            cycles += 1
            
            if (len(res) == 9):
                pi.write(10, 1)
                break
        clock_value_previous = clock_value_now
    return res
    

for i in range(60):
    print(rwbyte(16))

    #select += 1
    #sleep(0.1)
print("DONE")
pi.write(25,0)
pi.stop()


    
    
