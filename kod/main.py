# importing necessary modules
import ufirebase as firebase
from machine import Timer, Pin, ADC, RTC
import machine
import micropython

# Declearing variables and constants 
global adc
adc = 0
counter = 0
state = False
Sampling_Frequency = micropython.const(5) # 5ms = 200Hz

# Creating emergency buffer in case of failiure of TIMER
micropython.alloc_emergency_exception_buf(100)

# Declearing TIMER
timer_0 = Timer(0)

# Declearing input pin and configuring it
p34 = Pin(34, Pin.IN)
adc = ADC(p34)
adc.atten(ADC.ATTN_11DB) # 0 - 3.3V sampling
adc.width(ADC.WIDTH_12BIT) # 12 bit length data (For higher resolution)

# Declearing past values for Filtering purposes
xn1 = 0
xn2 = 0
xn3 = 0

yn1 = 0
yn2 = 0
yn3 = 0

yl1 = 0
yl2 = 0
yl3 = 0
yl4 = 0
yl5 = 0
yl6 = 0
yl7 = 0

xl1 = 0
xl2 = 0
xl3 = 0
xl4 = 0
xl5 = 0
xl6 = 0
xl7 = 0


# Creating Interrupt Service Routine function for decleare what to do in 
def isr(timer):
    global state
    global adcVal
    
    adcVal = adc.read_uv()/1000 # Converting mV to V
    state = True


# Initializing TIMER
timer_0.init(period = Sampling_Frequency, mode = Timer.PERIODIC, callback = isr)

# Creating infinite loop for data gathering
while True:
    if(state):

        xn = adcVal

        # 3rd Order Butterworth IIR High-Pass Filter Fs = 200 Hz Fc = 0.5 Hz         
        yn = xn - 3*xn1 + 3 * xn2 - 1 * xn3
        yn = yn + 2.9686*yn1 - 2.9377*yn2 + 0.9691*yn3
        
        xn3 = xn2
        xn2 = xn1
        xn1 = xn
        
        yn3 = yn2
        yn2 = yn1
        yn1 = yn
        
        xl0 = yn
        

        # 7th Order Butterworth IIR Low-Pass Filter Fs = 200 Hz Fc = 35 Hz
        yl0 = xl0*0.0023 + xl1*0.0161 + xl2 * 0.0483 + xl3 * 0.0805 + xl4 * 0.0805 + xl5 * 0.0483 + xl6 * 0.0161 + xl7 * 0.0023
        yl0 = yl0 + 2.0852 * yl1 - 2.6251 * yl2 + 1.9814 * yl3 - yl4*0.9997 + yl5 * 0.3187 - yl6*0.06 + yl7*0.005
        
        yl7 = yl6
        yl6 = yl5
        yl5 = yl4
        yl4 = yl3
        yl3 = yl2
        yl2 = yl1
        yl1 = yl0

        xl7 = xl6
        xl6 = xl5
        xl5 = xl4
        xl4 = xl3
        xl3 = xl2
        xl2 = xl1
        xl1 = xl0
        
        print(yl0, xn)
        state = False
