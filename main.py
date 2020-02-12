#!/usr/bin/python3
''' main.py '''

import RPi.GPIO as GPIO
import time, threading
from time import sleep
import global_objects
import periodic
import reader
import os.path



def init():
    global_objects.g_periodic_task_flags =  global_objects.NO_TASK
    
def init_ant():
    if not os.path.isfile("/var/tmp/ant.txt"):
        ant = open("/var/tmp/ant.txt", "w")
        ant.write("Use Antenna One")
        ant.close()
        print("Use Antenna One")
    
def main():
    # setup debug I/O
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)   
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    
    init()
#    reader.set_stcomm()
    # set up 50ms state machine function list
    periodic.set_st()
    reader.set_stcomm()
    reader.set_sttxrx()
    init_ant()
    
    # start 50ms timer thread
    periodic.timer0()
    reader.init_comm()
    
    #app.socketio.run(app, host='0.0.0.0', debug=False)
    
    while(1):
        periodic.periodic_main()
        reader.process_reader()
        pass

if __name__=="__main__":
    main()