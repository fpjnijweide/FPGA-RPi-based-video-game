from time import sleep
#import RPi.GPIO as GPIO
import psutil, os
import pigpio

p = psutil.Process(os.getpid())
p.nice(-19)

pi = pigpio.pi('Dragon47')

#GPIO.cleanup()
##GPIO.setmode(GPIO.BOARD)

#GPIO.setup(23, GPIO.OUT) #clock will be on pin 23
#clock = GPIO.PWM(23, 500) # hz
#clock.start(50) # start the clock witha  duty cycle of 50%

pi.set_PWM_frequency(11, 1000)
pi.set_PWM_dutycycle(11,110)
#GPIO.setup(19, GPIO.OUT) #slave select will be on pin 24

#GPIO.setup(40, GPIO.IN) #pin 40 used for input
#GPIO.setup(38, GPIO.OUT) #pin 38 used for output

pi.write(10, 1)
#GPIO.output(19, select)

def readinfo(pin):
    res = []
    cycles = 0
    #TODO find out if there is a neater way to detect clock than read pin
    clock_value_previous = pi.read(11) #GPIO.input(23)
    
    while True:
        clock_value_now = pi.read(11) #GPIO.input(23)
        if (clock_value_now != clock_value_previous and clock_value_now == 1):
            #cycles += 1
            #GPIO.output(19, 0)
            #res.append(GPIO.input(pin))
            pi.write(10, 0)
            res.append(pi.read(pin))
            
            pi.write(25, 1)
            
        if (len(res) == 9):
            pi.write(10, 1)
            #GPIO.output(19, 1)
            #sleep(0.1)
            
            break
        clock_value_previous = clock_value_now
    return res
    
        
for i in range(50):
    print(readinfo(16))
    #select += 1
    #sleep(0.1)
print("DONE")
pi.stop()


	
	
