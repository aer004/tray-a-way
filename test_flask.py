from flask import Flask, render_template, redirect, request
import tray
import time
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

global CURRENT_WEIGHT
CURRENT_WEIGHT = 10 #SET IN SETUP.PY, dummy value currently
global ALARM_MODE
ALARM_MODE = True  #True = LOUD False = silent
ALARM_DEFAULT = 30 # turn off alarm after 30 seconds, unless user turns it off with a tag
WEIGHT_THRESHOLD = 15 # depends on load cell sensitivity, in grams 
global WEIGHT_LOG
WEIGHT_LOG = [] # [{'weight': 14, 'time': 'May 2 1:15PM'}, ... ]
global TIME_DATE
TIME_DATE = None

# BCM pins
GPIO.setmode(GPIO.BCM)

#thread stuff
WEIGHT_LOCK = Lock()
ARMED_LOCK = Lock()
LOG_LOCK = Lock() # lock for the weight dictionary log

print("Welcome to the Tray-a-way") # Welcome message

#setup functions
print("Setting up components...") # debug message to show that we are loading functions
tray.buzzer_setup()
tray.nfc_setup()
tray.led_setup()
tray.load_cell_setup()

if (ALARM_MODE == True):
	print("You are in Loud Mode")
else:
	print("You are in Silent Mode")

#time and date
def get_time_date():
	global TIME_DATE
	TIME_DATE = datetime.today().strftime("%I:%M:%S %p") + date.today().strftime("%B %d, %Y")
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
	arm = "disabled"
	disarm = ""
	loud = "disabled"
	silent = ""
	if ARMED == True:
		arm = ""
		disarm = "disabled"
	elif ARMED == False:
		arm = "disabled"
		disarm = ""
	if ALARM_MODE == True:
		loud = ""
		silent = "disabled"
	elif ALARM_MODE == False:
		loud = "disabled"
		silent = ""
	return render_template("alarm.html", armdisabled = arm, disarmdisabled = disarm, louddisable = loud, silentdisable = silent)

@app.route("/alarm/<int:action>")
def alarm_act(action):
	global ARMED
	global ALARM_MODE
	with ARMED_LOCK:
		if action == 0:
			ARMED = True
		elif action == 1:
			ARMED = False
			tray.buzzer_off()
		elif action == 2:
			ALARM_MODE = True
		elif action == 3:
			ALARM_MODE = False
	return redirect("/templates/alarm")

@app.route("/templates/logdata")
def logdata_template():
	d = WEIGHT_LOG
	return render_template("logdata", hist = d)

app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
