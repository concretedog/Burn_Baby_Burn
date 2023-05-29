from machine import Pin, PWM
from time import sleep



pwm = PWM(Pin(15, pull=Pin.PULL_DOWN)) #Pin 15 is connected to the "s" input on the Burn Baby Burn. 

pwm.freq(500)

while True: #Turns on and off the Burn Baby Burn coil for 3 seconds on, 3 seconds off. 
    pwm.duty_u16(0)
    sleep(3)
    pwm.duty_u16(60000)
    sleep(3)
    
    
