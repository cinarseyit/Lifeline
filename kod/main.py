from machine import Timer, Pin, ADC, RTC
import machine
import micropython
import time

global adc

adc = 0
count = 0
state = False
instance1 = 0
timer = 0
count = 0
flag = 0
threshold = 700
hr = 72
hrv = 0
interval = 0

micropython.alloc_emergency_exception_buf(100)

Sampling_Frequency = micropython.const(5) # 5ms = 200Hz 
timer_0 = Timer(0)

p34 = Pin(34, Pin.IN)
adc = ADC(p34)

adc.atten(ADC.ATTN_11DB) # 0 - 3.3V sampling
adc.width(ADC.WIDTH_12BIT)


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



def isr(timer):
    
    global state
    global adcVal
    
    adcVal = adc.read_uv()/1000
    state = True

timer_0.init(period = Sampling_Frequency, mode = Timer.PERIODIC, callback = isr)


while True:
    
    if(state):
        
            xn = adcVal
        
            yn = xn - 3*xn1 + 3 * xn2 - 1 * xn3
            yn = yn + 2.9686*yn1 - 2.9377*yn2 + 0.9691*yn3
        
            xn3 = xn2
            xn2 = xn1
            xn1 = xn        
        
            yn3 = yn2
            yn2 = yn1
            yn1 = yn
        
            xl0 = yn
        
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
            
            if yl0 > threshold and flag == 0:
                
                count += 1
                flag = 1
                interval = time.ticks_diff(time.ticks_us(), instance1)
                instance1= time.ticks_us()
                
            elif yl0 < threshold:
                
                flag = 0
            
            if time.ticks_diff(time.ticks_ms(), timer) > 3200:
                
                hr = count*15
                timer = time.ticks_ms()
                count = 0;
       
            
            print(yl0, xnr)
            
            state = False
        

