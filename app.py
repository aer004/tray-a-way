from flask import Flask, render_template, redirect, request
import tray
import time
from datetime import date, datetime
from queue import Queue
from threading import Thread, Lock, Event
import RPi.GPIO as GPIO

# Constants
global ARMED
ARMED = True

"""
ARMED = True is the default since the Tray-a-way should be tracking for weight changes
When ARMED = True, this means that the alarm (silent or loud) will go off if there is a weight change
When ARMED = False, this means that the alarm will not go off since the user has a successful scan
"""

global SETUP 
SETUP = False # using to fix the Flask!

global CURRENT_WEIGHT
CURRENT_WEIGHT = 10 #SET IN SETUP.PY, dummy value currently
global ALARM_MODE
ALARM_MODE = False  #True = LOUD False = silent
ALARM_DEFAULT = 30 # turn off alarm after 30 seconds, unless user turns it off with a tag
WEIGHT_THRESHOLD = 15 # depends on load cell sensitivity, in grams 
global WEIGHT_LOG
WEIGHT_LOG = [] # [{'weight': 14, 'time': '03:19:32 PM May 09, 2022'}, ... ]
global TIME_DATE
TIME_DATE = None

# BCM pins
GPIO.setmode(GPIO.BCM)

#thread stuff
WEIGHT_LOCK = Lock()
ARMED_LOCK = Lock()
LOG_LOCK = Lock() # lock for the weight dictionary log

print("Welcome to the Tray-a-way") # Welcome message


def print_alarm_setting():
	if (ALARM_MODE == True):
		print("You are in Loud Mode")
	else:
		print("You are in Silent Mode")

#time and date
def get_time_date():
	global TIME_DATE
	TIME_DATE = datetime.today().strftime("%I:%M:%S %p ") + date.today().strftime("%B %d, %Y")
	return TIME_DATE

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
	return redirect("/templates/index")

@app.route("/templates/index")
def home_template():
	return render_template("index.html")

@app.route("/templates/alarm")
def alarm_template():
	global ARMED
	global ALARM_MODE
	arm = "disabled"
	disarm = ""
	loud = "disabled"
	silent = ""
	if ARMED == True:
		arm = "disabled"
		disarm = ""
	elif ARMED == False:
		arm = ""
		disarm = "disabled"
	if ALARM_MODE == True: # loud mode, we want loud button to now be disabled since we're at that setting
		loud = "disabled"
		silent = ""
	elif ALARM_MODE == False: # silent mode, can press Loud button to switch
		loud = ""
		silent = "disabled"
	return render_template("alarm.html", armdisabled = arm, disarmdisabled = disarm, louddisable = loud, silentdisable = silent)

@app.route("/alarm/<int:action>")
def alarm_act(action):
	global ARMED
	global ALARM_MODE
	with ARMED_LOCK:
		if action == 0:
			ARMED = True
			print("Tray is activated")
		elif action == 1:
			ARMED = False
			print("Tray is deactivated") # debug message for terminal
			tray.led_off()
			tray.buzzer_off()
		elif action == 2:
			ALARM_MODE = True
			print("Set to Loud Alarm")
		elif action == 3:
			ALARM_MODE = False
			print("Set to Silent Alarm")
	return redirect("/templates/alarm")

@app.route("/templates/logdata")
def logdata_template():
	d = WEIGHT_LOG
	return render_template("logdata.html", hist = d)


def check_armed():
	global ARMED
	global CURRENT_WEIGHT
	while True:
		with ARMED_LOCK:
			with WEIGHT_LOCK:
				scan = tray.read_nfc() 
				if ARMED == False: # tray is deactivated
					if scan: # successful scan, user wants to reactivate the tray
						CURRENT_WEIGHT = tray.measure_weight()
						ARMED = True
						print("Scanned = True, User reactivated tray")
						tray.white_led()
						time.sleep(3)
						tray.led_off()
					# else: tray is deactivated so do nothing

				else: # ARMED = True, have to check if the user wants to deactivate or not
					# if scan == False: # not tag was scanned (wrong ID or no tag, aka not the user)
						# print("Tray is activated, will trigger alarm")
						# don't need this since we don't want the terminal to keep indicating the tray is working
					if scan: # scan = True, successful scan
						# user wants to deactivate tray to safely use without triggering alarm
						ARMED = False 
						tray.buzzer_off()
						print("Scanned = True, User deactivated tray")
						tray.green_led()
						time.sleep(3)
						tray.led_off()

def check_weight():
	global ARMED
	global CURRENT_WEIGHT
	global ALARM_MODE
	global TIME_DATE
	while True:
		with ARMED_LOCK: # editing ARMED variable
			with WEIGHT_LOCK: # editing current weight
				new_weight = tray.measure_weight()
				if ARMED == True: # alarm is on
					if abs(new_weight - CURRENT_WEIGHT) > WEIGHT_THRESHOLD:
						with LOG_LOCK: # editing dictionary
							tray.red_led() # turn on led to signal weight change
							CURRENT_WEIGHT = tray.measure_weight()
							TIME_DATE = get_time_date()
							WEIGHT_LOG.append({'weight': CURRENT_WEIGHT, 'time': TIME_DATE})
							if ALARM_MODE == True: # loud mode
								tray.buzzer_on()
								print("Loud Alarm, passed weight threshold")
								curr_time = 0 # start at 0 seconds
								while (curr_time < ALARM_DEFAULT): # keep buzzer on for 30 seconds unless the user scans the tag
									time.sleep(1) # pass 1 second
									curr_time += 1 # increment by 1 second
									user = tray.read_nfc()
									if user: # correctly scanned to turn off alarm during loud mode
										print("User scanned; deactivating alarm...")
										tray.buzzer_off()
										break # break out of while loop
								tray.buzzer_off() # turn off buzzer after 30 seconds default
							else: # ALARM_MODE == False # silent mode, debug statements for demo
								print("Silent Alarm, passed weight threshold")
							tray.led_off()
				else: # ARMED == False, user deactivated the alarm
					if abs(new_weight - CURRENT_WEIGHT) > WEIGHT_THRESHOLD:
			    			print("Passed the weight threshold, but user deactivated the alarm")
						# just debug statement for demo testing to see what state we're in 

if __name__ == "__main__":
	print_alarm_setting() # tells user what alarm setting they are on initially
	if (SETUP == False):   
		print("Setting up components...") # debug message to show that we are loading functions
		tray.buzzer_setup()
		print("Buzzer done")
		tray.nfc_setup() # not setting up
		print("NFC done")
		tray.led_setup()
		print("LED done")
		tray.load_cell_setup()
		print("Finished setup*")
		SETUP = True
	
	t1 = Thread(target=check_armed)
	t1.start()
	t2 = Thread(target=check_weight)
	t2.start()

	print("Starting app")
	app.run(host='0.0.0.0', port=80, debug=False, threaded=True)


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
- alarm goes off (red)
"""
