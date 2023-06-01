"""
    GPIO pin 0 is connected to the "s" signal pin on the "Burn Baby Burn".
    A pull pin switch (remove pin to make) is tied between the pulled low GPIO pin 15 on the RP2040 and the positive rail.
    Note that one of the - connections on the "Burn Baby Burn" needs to be connected to the RP2040/Pico GND rail.
"""

from micropython import schedule
from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(0,pull=Pin.PULL_DOWN)) # Pin 0 attached to the Nicrome Burner, initialising low to avoid premature heating.
pwm.freq(500)                        # 500Hz has tested as fine. 
pwm.duty_u16(0)                      # Initial burner as off.
FIRED_STATE=0                        # State variable used to ensure single firing of burner.

print("not deployed")

def Baby_IRQ(pin):
    pin.irq(handler=None)    # Turn off the handler, avoiding bounce, first rising edge is sufficient.
    schedule(Burn_Baby_Burn,None) # Schedule the long running stuff to happen soon.

def Burn_Baby_Burn(Fired_State):        # scheduled by the IRQ to do the relatively long running stuff outside the contraints of interrupt handler.
    global FIRED_STATE
   
    if FIRED_STATE==0:       # only burn if previously unfired
        FIRED_STATE = 1      # prevent retriggers
        #pwm.duty_u16(0)
        sleep(2)             # delay between pin pull and burner firing in seconds
        pwm.duty_u16(65025)  # PWM value which defines how much current can flow/how hot the burner becomes. Expects a value between 0 and 65025
        print("firing")
        sleep(4)             # duration of the firing in seconds
        print("fired")
        pwm.duty_u16(0)      # Turn off the burner
        


Drop_Pin = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN) # Pull pin switch on pin 15, internal pull down used.
Drop_Pin.irq(trigger=machine.Pin.IRQ_RISING, handler=Baby_IRQ)  # Pull pin hardware configured to cause a rising edge.