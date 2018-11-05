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

    pi.write(constants.SLAVESELECT_PIN, 1)  # make sure no data is sent yet

    pi.wave_clear() # clear any existing waveforms

    # flash_500=[]
    # flash_500.append(pigpio.pulse(1<<constants.CLOCK_PIN, 1<<20, 10))
    # #flash_500.append(pigpio.pulse(1<<G2, 1<<G1, 500000))
    # pi.wave_add_generic(flash_500) # 500 ms flashes