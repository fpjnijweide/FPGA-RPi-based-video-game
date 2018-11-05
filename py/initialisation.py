import psutil, os
import pigpio
import constants
from subprocess import call

def initConnection():
    global pi
    #START DAEMON
    
    call(["sudo", "pigpiod"])

    # STARTING PROCESS, SET PRIORITY
    p = psutil.Process(os.getpid())  
    p.nice(-19) # make process high priority
    pi = pigpio.pi('Dragon47')

    # #Init pins
    # for readpin in constants.READ_PINS:
    #     pi.set_mode(readpin[1], pigpio.INPUT)
    #
    # for writepin in constants.WRITE_PINS:
    #     pi.set_mode(writepin[1], pigpio.OUTPUT)
    # pi.set_mode(constants.CLOCK_PIN, pigpio.OUTPUT)
    # pi.set_mode(constants.MOSI_PIN, pigpio.OUTPUT)


    # Starting clock
    pi.set_PWM_frequency(constants.CLOCK_PIN, constants.CLOCKSPEED)
    pi.set_PWM_dutycycle(constants.CLOCK_PIN, constants.DUTYCYCLE)

    pi.write(constants.MOSI_PIN, 1)  # make sure no data is sent yet