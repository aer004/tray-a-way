from flask import Flask, render_template, redirect, request
import random

global ARMED
ARMED = None

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

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
