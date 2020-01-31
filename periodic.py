''' periodic.py '''

import time, threading
from time import sleep
import RPi.GPIO as GPIO
import global_objects
import reader_vars

ro = reader_vars.ReaderVars

global toggle
toggle = 0
global toggle100
toggle100 = 0
global toggle500
toggle500 = 0
global toggle1S
toggle1S = 0
global sv
sv = 0
global st
st = 0
global cs
cs = 0
global seconds
seconds = 5

def periodic_main():
#    global TASK_50MS
    if(global_objects.g_periodic_task_flags & global_objects.TASK_50MS):
        task_50ms()
        global_objects.g_periodic_task_flags &= ~global_objects.TASK_50MS

#    global TASK_100MS
    if(global_objects.g_periodic_task_flags & global_objects.TASK_100MS):
        task_100ms()
        global_objects.g_periodic_task_flags &= ~global_objects.TASK_100MS
     
#    global TASK_500MS
    if(global_objects.g_periodic_task_flags & global_objects.TASK_500MS):
        task_500ms()
        global_objects.g_periodic_task_flags &= ~global_objects.TASK_500MS
     
#    global TASK_1SEC
    if(global_objects.g_periodic_task_flags & global_objects.TASK_1SEC):
        global_objects.g_periodic_task_flags &= ~global_objects.TASK_1SEC
        task_1SEC()
        
     

    # other if's on TASK_100MS etc. task flags to see if task is performed

def task_50ms():       
    # continue on with switch selection of 50ms time slots
    # uses a state machine
    #f = st[sv]()
    f = st[sv]
    f()

def time_slot0():
    global sv
    GPIO.output(12, GPIO.HIGH)
    sv = 1
           
def time_slot1():
    global sv
    GPIO.output(12, GPIO.LOW)
    sv = 2
         
def time_slot2():
    global sv
    GPIO.output(12, GPIO.HIGH)
    sv = 3
        
def time_slot3():
    global sv
    GPIO.output(12, GPIO.LOW)
    sv = 4
        
def time_slot4():
    global sv
    GPIO.output(12, GPIO.HIGH)
    sv = 5
 
def time_slot5():
    global sv
    GPIO.output(12, GPIO.LOW)
    sv = 0

def set_st():
    global st
    st = [time_slot0, time_slot1, time_slot2, time_slot3, time_slot4, time_slot5]
#    print("set_st", st)
    
# list of functons
def get_st():
    global sv
    global st
    global cs
    
    cs = st[sv]
#    print('get_st= ', cs)
    return cs

def task_100ms():
    global toggle100
    toggle100 ^= 1
    if(toggle100):
#        GPIO.output(26, GPIO.HIGH)
        pass
    else:
#        GPIO.output(26, GPIO.LOW)        
        pass        
    pass

def task_500ms():
    global toggle500
    toggle500 ^= 1
    if(toggle500):
#        GPIO.output(26, GPIO.HIGH)
        pass
    else:
#        GPIO.output(26, GPIO.LOW)
    # check that threads are not growing
#    print(threading.active_count(), end=' ') 
        pass

def task_1SEC():
    global toggle1S
    global seconds
    toggle1S ^= 1
    if(toggle1S):
        GPIO.output(5, GPIO.HIGH)
    else:
        GPIO.output(5, GPIO.LOW)
    # test fire off reader comm state machine once per second
#    ro.reader_txrx_states |= ro.READER_TXRX_TX
    if(seconds > 0):
        seconds -= 1
    else:
#        ro.reader_comm_states |= ro.READER_COMM_CONNECTING
        ro.reader_txrx_states |= ro.READER_TXRX_TX
#        print('s', end=' ')
        seconds = 5
    pass
    



# main 25ms timer    
def timer0():
#    timer.cancel()
    threading.Timer(.012, timer0).start()
    # Debug I/O signal
#    GPIO.setup(6, GPIO.OUT)
    GPIO.output(6, GPIO.HIGH)
#    sleep(0.01) # this allows a wider timing pulse to see on o'scope
    GPIO.output(6, GPIO.LOW)
    
    if (global_objects.g_periodic_task_flags != global_objects.NO_TASK ):
        # some task did not complete; this is timer overrun condition
#        print("Timer task overrun error!!! %x" % global_objects.g_periodic_task_flags )
        pass
    
    # bump 25ms timer counter
    global_objects.g_per25ms_counter += 1
    if (global_objects.g_per25ms_counter >= 2):
        global_objects.g_per25ms_counter = 0
        # schedule 50ms timer task
        global_objects.g_periodic_task_flags |= global_objects.TASK_50MS
       
        global_objects.g_per100ms_counter += 1
        if (global_objects.g_per100ms_counter >= 2):
            # schedule 100ms task
            global_objects.g_periodic_task_flags |= global_objects.TASK_100MS
            global_objects.g_per100ms_counter = 0
            
            global_objects.g_per500ms_counter += 1
            if (global_objects.g_per500ms_counter >= 5):
                global_objects.g_per500ms_counter = 0            
                # schedule 500ms task
                global_objects.g_periodic_task_flags |= global_objects.TASK_500MS
            
                global_objects.g_per1SEC_counter += 1
                if (global_objects.g_per1SEC_counter > 1):
                    global_objects.g_per1SEC_counter = 0
                    global_objects.g_periodic_task_flags |= global_objects.TASK_1SEC
              

                

                
            