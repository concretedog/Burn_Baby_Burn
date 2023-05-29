"""
    GPIO pin 0 is connected to the "s" signal pin on the "Burn Baby Burn".
    A pull pin switch (remove pin to make) is tied between the pulled low GPIO pin 15 on the RP2040 and the positive rail.
    Note that one of the - connections on the "Burn Baby Burn" needs to be connected to the RP2040/Pico GND rail.
"""


from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(0,pull=Pin.PULL_DOWN)) #set up GPIO pin 0 as a PWM pin initialising it pulled low

pwm.freq(500) #Set PWM Frequency, 500 has tested as fine. 
pwm.duty_u16(0) #Set initial duty cycle at zero

fired_state=0 #Initialise a variable set to zero

print("not deployed")

def Burn_Baby_Burn(fire): #Interrupt handler will run when irq conditions are met
    global fired_state	#reference the value of fired_state (check if we have fired before)
    Drop_Pin.irq(handler=None) # Turn off the handler while it is executing avoid bounce
   
    if (Drop_Pin.value()==1) and (fired_state==0):#pull pin is high and fired state is zero/unfired
        #pwm.duty_u16(0)
        sleep(2) #duration between pin pulled and burner firing in seconds
        pwm.duty_u16(65025) #PWM value which defines how much current can flow/how hot the burner becomes. Expects a value between 0 and 65025
        print("firing")
        sleep(4) #duration of the firing in seconds
        fired_state = 1 #set fired_state as 1 therefore any attempted accidental retriggers will be aborted
        print("fired")
        pwm.duty_u16(0) #Turn off the burner
        
    #elif (Drop_Pin.value()==1) and (fired_state==1): #if pull pin is high and fired state is high/fired then do nothing. 
        #pwm.duty_u16(0)



Drop_Pin = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN) #Create an object for our pull pin switch change of state
Drop_Pin.irq(trigger=machine.Pin.IRQ_RISING, handler=Burn_Baby_Burn) #Setup the irq with what triggers the interupt and point to the handler
