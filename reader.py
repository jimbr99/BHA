''' process_reader.py '''

import time, threading
from time import sleep
import RPi.GPIO as GPIO
import global_objects
import reader_vars
import reader_main

# defs global to this module
READER_COMM_IDLE = 0
READER_COMM_CONNECTING = 1
READER_COMM_CONNECTED = 2
READER_COMM_ABORT = 3

READER_TXRX_IDLE = 0

READER_RX_IDLE = 0

READER_ABORT_IDLE = 0

# local global vars
global reader_comm_states  # comm state flags
global reader_tx_states    # tx state flags
global reader_rx_states    # rx state flags
global reader_abort_states # abort state flags

global st_comm
global sv
global toggleTX

toggleTX = 0
sv = READER_COMM_IDLE
ro = reader_vars.ReaderVars

''' process checks to see if comm is not idle and if true
    then switches to the current state to continue processing
    items in the state machine.
'''
def init_comm():
    ro.reader_comm_states = ro.READER_COMM_IDLE | ro.READER_TXRX_IDLE
    
def process_reader():
    if(ro.reader_comm_states != ro.READER_COMM_IDLE):       
        reader_comm_sm()
        # restore idle following comm processing
        ro.reader_comm_states = ro.READER_COMM_IDLE
    if(ro.reader_txrx_states != ro.READER_TXRX_IDLE):
        reader_txrx_sm()        
        # restore idle following reader processing
     #   ro.reader_txrx_states = ro.READER_TXRX_IDLE
    '''
    if(reader_vars.reader_rx_states != reader_vars.READER_RX_IDLE):
        pass
    if(reader_vars.reader_abort_states != reader_vars.READER_ABORT_IDLE):
        pass
    '''

''' switches to the current state using sv (state index)
    and st (function list) arguments. '''
def switch_sm(sv, st):
    f = st[sv] # get current state function address
    f() # call current state


''' ******** Communication state machine ******** '''   
def reader_comm_sm():
 #   print("comm sm", end = '')
 #   print(ro.reader_comm_states)
 #   c = rshift_cnt(ro.reader_comm_states)
    ro.sv_comm = ro.reader_comm_states
 #   print('ro.sv_comm=',ro.sv_comm, end = ' ')
    
    # use switch function to select current state in target state machine
    switch_sm(ro.sv_comm, ro.st_comm)    

''' Serial Communication states '''
''' parking state that does nothing; other agents must monitor for errors '''
def reader_comm_idle(): 
    global sv
    global st
#    print("reader comm idle")
    sleep(0.01)
    pass

def reader_comm_connecting():
#    print("reader comm connecting")
    ro.sv_comm = ro.READER_COMM_CONNECTED
    ro.reader_comm_states = ro.sv_comm   
    pass

def reader_comm_connected():
#    print(".", end="")
#    ro.sv_comm = ro.READER_COMM_ABORT
 #   ro.reader_comm_states = ro.sv_comm
    sleep(2.0)
    pass

def reader_comm_abort():
#    print("reader comm abort")
    ro.sv_comm = ro.READER_COMM_IDLE
    ro.reader_comm_states = ro.sv_comm
    pass

def set_stcomm(): # generate list of state machine vectors
    ro.st_comm = [reader_comm_idle, reader_comm_connecting, reader_comm_connected, reader_comm_abort]   
    ro.sv_comm = ro.READER_COMM_IDLE # init to idle state
#    print("set_st_comm: ", ro.st_comm)
    
###############################################################
''' reader rxtx state machine '''
def reader_txrx_sm():
    ro.sv_txrx = ro.reader_txrx_states
#    print(ro.sv_txrx, end=' ')
    # use switch function to select current state in target state machine
    switch_sm(ro.sv_txrx, ro.st_txrx)
#    ro.reader_txrx_states = ro.READER_TXRX_IDLE
#    print("reader txrx state machine", end=' ')
    pass

''' reader is idle '''
def reader_idle():
    pass

''' reader is transmitting command '''
def reader_tx():
    ro.sv = ro.READER_TXRX_TX
    ro.reader_txrx_states = ro.sv_txrx
#    print("!", end=' ')
    GPIO.output(26, GPIO.HIGH)
    reader_main.reader_main()  # sleep(0.1)
    GPIO.output(26, GPIO.LOW)
    ro.sv = ro.READER_TXRX_RX # transition to RX processing state
    ro.reader_txrx_states = ro.READER_TXRX_RX
    
    '''
    global toggleTX
    toggleTX ^= 1
    if(toggleTX):
#        GPIO.output(26, GPIO.HIGH)
        pass
    else:
#        GPIO.output(26, GPIO.LOW)
        pass
#    sleep(0.01)
    '''
    
    pass

''' reader is receiving and processing response '''
def reader_rx():
    ro.sv = ro.READER_TXRX_RX
    ro.reader_txrx_states = ro.sv_txrx
    reader_main.reader_process_rx()
    ro.reader_txrx_states = ro.READER_TXRX_IDLE
    pass

''' reader is aborting due to error/reset '''
def reader_abort():
    ro.sv = ro.READER_TXRX_ABORT
    ro.reader_txrx_states = ro.sv_txrx
    pass

''' set_st() makes list of reader idle, tx, rx, and abort states for use
    by switch_sm function '''    
def set_sttxrx():
    ro.st_txrx = [reader_idle, reader_tx, reader_rx, reader_abort]
#    print("set_st: ", ro.st)
    pass


def reader_process_rx():
#    print('Processing data.....')
    pass
    





def rshift_cnt(val):
    n=1
    while n < 8:
        if val & 1:
            return n
        else:
            val = val>>1
        n += 1
    if n == 7:
        return 0
    

    