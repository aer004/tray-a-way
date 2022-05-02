from flask import Flask, render_template, redirect, request
import tray
import time
from queue import Queue
from threading import Thread, Lock, Event

# Constants
global ARMED
ARMED = True

"""
ARMED = True is the default since the Tray-a-way should be tracking for weight changes

When ARMED = True, this means that the alarm (silent or loud) will go off if there is a weight change
When ARMED = False, this means that the alarm will not go off since the user has a successful scan
"""

global CURRENT_WEIGHT
CURRENT_WEIGHT = 10 #SET IN SETUP.PY
global ALARM_MODE
ALARM_MODE = False #True = LOUD False = silent
WEIGHT_THRESHOLD = 4 # depends on load cell sensitivity
global WEIGHT_LOG
WEIGHT_LOG = [] #[[TIME, DATE, WEIGHT], ... ]

WEIGHT_LOCK = Lock()
buzzer_setup()
nfc_setup()


# def check_armed():
#  global ARMED
#  global CURRENT_WEIGHT
#  while True:
#   scan = tray.read_nfc()
#   if scan == None: #Case: scan timedout
#    set.led(white, forever)
#    ARMED = True
#   elif scan == False: #Case: scan unsuccessful
#    set.led(red, 4) #4 seconds?
#    ARMED = True
#   elif scan == uid:
#    if ARMED == True:
#     #CHECK IF UID IS THE RIGHT ID?
#     ARMED = False
#     set.led(green, forever)
#    else: #ARMED == False
#     CURRENT_WEIGHT = get.weight() #fake function
#     ARMED = True
#     set.led(white, forever)

# def check_weight():
#  global ARMED
#  global CURRENT_WEIGHT
#  global ALARM_MODE
#  while True:
#    if ARMED == True:
#     if abs(get.weight() - CURRENT_WEIGHT) < WEIGHT_THRESHOLD: #check depending on sensitivity
#      if ALARM_MODE == True:
#       play_buzzer() #set time and lskedfjalskdjnbhd
#      record time and weight
    
   
t1 = Thread(target=check_armed)
t1.start()
t2 = Thread(target=check_weight)
t2.start()

t1.join()
t2.join()
  
# Thread for continuously monitoring the NFC reader

# Thread for checking if it is armed 


"""
Issue: https://github.com/rb2468/tray-a-way/issues/72
 -- import libraries
 -- define an empty function for each task
 
What we need:
Continuously monitor if anything scanned
Continuously monitor any weight changes
- have an initial weight to detect changes
- document the weight change (time)
- silent alarm/loud alarm

Infinite loop

check if armed (true or false depending on scan)
if armed: detect the weight
if a specific amount of weight was changed then document it, and set off an alarm (true or false)
else: no change
Continuously monitor if anything scanned
- changes armed vs. disarmed (true or false)
- if disarmed:
- do nothing if there are weight changes

One thread constantly checking the state of the LED
- 3 states:
- armed (white)
- disarmed (green)
- failure to scan (red) # might not need the red LED since the loop will constantly check scan
"""
