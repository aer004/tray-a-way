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

#thread stuff...
WEIGHT_LOCK = Lock()

#setup functions
buzzer_setup()
nfc_setup()
led_setup()
load_cell_setup()

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
	return redirect("/templates/index")

@app.route("/templates/index")
def home_template():
	return render_template("index.html")

@app.route("/templates/alarm")
def alarm_template():
	arm = "disabled"
	disarm = ""
	if ARMED == True:
		arm = ""
		disarm = "disabled"
	elif ARMED == False:
		arm = "disabled"
		disarm = ""
	return render_template("alarm.html", armdisabled = arm, disarmdisabled = disarm)

@app.route("/alarm/<int:action>")
def alarm_act(action):
	global ARMED
	if action == 0:
		ARMED = True
	elif action == 1:
		ARMED = False
	return redirect("/templates/alarm")

@app.route("/templates/logdata")
def logdata_template():
	d = [{'weight': 14, 'time': 'May 2 1:15PM'}]
	return render_template("logdata", hist = d)


def check_armed():
	global ARMED
	global CURRENT_WEIGHT
	while True:
		scan = tray.read_nfc()
		if scan == None:
			tray.white_led()
			ARMED = True
		elif scan == False:
			tray.red_led()
			sleep(3)
			tray.white_led()
		elif scan == uid:
			if ARMED == True:
				ARMED = False
				tray.green_led()
			else:
				CURRENT_WEIGHT = measure_weight()
				ARMED = True
				white_led()

def check_weight():
	global ARMED
	global CURRENT_WEIGHT
	global ALARM_MODE
	while True:
		new_weight = get_weight()
		if ARMED == True:
			if abs(new_weight - CURRENT_WEIGHT) > WEIGHT_THRESHOLD:
				if ALARM_MODE = True:
					buzzer_on() #NEED TO TURN IT OFF??
				CURRENT_WEIGHT = measure_weight() #CURRENT TIME?? DEFAULT WEIGHT SET IN SETUP
				WEIGHT_LOG.append({'weight': CURRENT_WEIGHT, 'time': TIME_DATE})
    
   
t1 = Thread(target=check_armed)
t1.start()
t2 = Thread(target=check_weight)
t2.start()

app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

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
