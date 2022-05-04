import RPi.GPIO as GPIO
import pigpio
import time
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from py532lib.mifare import *
from hx711 import HX711
import random

# Buzzer Constants
BUZZ_FREQ = 4000
HALF_DUTY = 500000
ZERO_DUTY = 0
PWM_PIN = 13

# LED Pins
RED_PIN = 19 
GREEN_PIN = 12
BLUE_PIN = 18

GPIO.setmode(GPIO.BCM) # using bcm pins
GPIO.setwarnings(False) # to avoid potential error message

# NFC Constants
NFC_TIMEOUT = 5
NFC_MAX_TRIES = 1

# Load Cell Constants
LOAD_CELL_REFERENCE_UNIT = 100
LOAD_CELL_DATA_PIN = 5
LOAD_CELL_CLOCK_PIN = 6
WEIGHT_DELAY = 2 # delay for measuring each weight

def buzzer_setup():
	"Sets up pi varible for pigpio library"
	global pi
	pi = pigpio.pi()

def buzzer_on():
	"Turns buzzer on"
	pi.hardware_PWM(PWM_PIN, BUZZ_FREQ, HALF_DUTY)

def buzzer_off():
	"Turns buzzer off"
	pi.hardware_PWM(PWM_PIN, BUZZ_FREQ, ZERO_DUTY)

def nfc_setup():
        global nfc_tag
        nfc_tag = Mifare() # using a NFC Mifare 1 tag
        nfc_tag.SAMconfigure() # configure the NFC tag
        nfc_tag.set_max_retries(NFC_MAX_TRIES) # only searching for a tag once

def read_nfc():
	t_end = time.time() + NFC_TIMEOUT
	card_read = None
	"""
	if card_read = False, then there was an unsuccessful scan (either wrong tag or no scan -- pn532 library can't differentiate the two 
	if card_read = UID, then there was a successful scan
	"""
	
	while (time.time() < t_end):
		uid = nfc_tag.scan_field() # will either return UID (successful) or False (unsuccessful)
		if uid:
			# successful scan
			return uid
	# pn532 library is unable to differentiate between the wrong tag or no scan (it just returns the same variable, False)
	# only returns UID for the correct ID used
	return False # unsuccessful scan attempt 

def led_setup():
	## Red LED
	GPIO.setup(RED_PIN, GPIO.OUT)
	GPIO.output(RED_PIN, GPIO.HIGH)

	## Green LED
	GPIO.setup(GREEN_PIN, GPIO.OUT)
	GPIO.output(GREEN_PIN, GPIO.HIGH)

	## Blue LED
	GPIO.setup(BLUE_PIN, GPIO.OUT)
	GPIO.output(BLUE_PIN, GPIO.HIGH)

# Failure to Scan Tag
def red_led():
	GPIO.output(RED_PIN, GPIO.LOW)
    

# ARMED = False, (Disarmed) -- Let the user safely use the tray
def green_led():
	GPIO.output(GREEN_PIN, GPIO.LOW)
    

# ARMED = True, Working Tray
def white_led():
	GPIO.output(BLUE_PIN, GPIO.LOW)
	GPIO.output(GREEN_PIN, GPIO.LOW)
	GPIO.output(RED_PIN, GPIO.LOW)

def led_off():
	GPIO.output(RED_PIN, GPIO.HIGH)
	GPIO.output(GREEN_PIN, GPIO.HIGH)
	GPIO.output(BLUE_PIN, GPIO.HIGH)

# Sets up load cell variables and calibrates it
def load_cell_setup():
	global hx
	hx = HX711(LOAD_CELL_DATA_PIN, LOAD_CELL_CLOCK_PIN)
	hx.set_reading_format("MSB","MSB")
	hx.set_reference_unit(LOAD_CELL_REFERENCE_UNIT)
	hx.reset()
	hx.tare()

# Obtains weight in grams
def measure_weight():
	global WEIGHT_DELAY
	val = hx.get_weight(5)
	if (val < 0):
		val = 0
	print("Weight: ", val)
	time.sleep(WEIGHT_DELAY)
	return val

def dummy_measure_weight():
	global WEIGHT_DELAY
	val = random.randint(40,50)
	print("Weight: ", val)
	time.sleep(WEIGHT_DELAY)
	return val # change for delay (went too fast)


# Functions for testing the buzzer
# frequency_chart = {"C_5": 523, "CS_5": 554, "D_5": 587, "DS_5": 622, "E_5": 659, "F_5": 698, "FS_5": 740, "G_5": 784, "GS_5": 831, "A_5": 880, "AS_5": 932, "B_5": 988, "C_6": 1047, "CS_6": 1109, "D_6": 1175, "DS_6": 1245, "E_6": 1319, "F_6": 1397, "FS_6": 1480, "G_6": 1568, "GS_6": 1661, "A_6": 1760, "AS_6": 1865, "B_6": 1976, "C_7": 2093, "CS_7": 2217, "D_7": 2349, "DS_7": 2489, "E_7": 2637, "F_7": 2794, "FS_7": 2960, "G_7": 3136, "GS_7": 3322, "A_7": 3520, "AS_7": 3729, "B_7": 3951}

# def play_tone(tone):
# 	"Plays buzzer at certain tone, which is give in frequency"
# 	pi.hardware_PWM(PWM_PIN, tone, HALF_DUTY)

# def play_song(song, tempo):
# 	"""
# 	Input is a list with a list for every note. 
# 	The zeroth index of the inner lists (song[i][0]) are keys for the frequency dictionary, 
# 	which have values in Hz for each midi note. 
# 	Then, the first index of the inner lists (song[i][1]) is the amount of 
# 	durations the note should be played. 
# 	To change that to seconds, the durations have to be multipled by the tempo, 
# 	which is in milliseconds, so then the resulting value has to be divided by 1000.
# 	"""
# 	for i in range(len(song)): #go through length of input list
# 	        play_tone(frequency_chart[song[i][0]]) #play tone from frequency dictionary
# 		time_seconds = (song[i][1] * tempo)/1000
# 		time.sleep(time_seconds) #let tone play for given time
# def play_harry():
# 	"Plays harry potter theme song using play_song function"
# 	harry_midi = [["B_5", 120], ["E_6", 180], ["G_6", 60], ["FS_6", 120], ["E_6", 240], ["B_6", 120], ["A_6", 255], ["A_6", 105], ["FS_6", 255], ["FS_6", 105], ["E_6", 180], ["G_6", 60], ["FS_6", 120], ["D_6", 240], ["F_6", 120], ["B_5", 255], ["B_5", 255], ["B_5", 210], ["E_6", 180], ["G_6", 60], ["FS_6", 120], ["E_6", 240], ["B_6", 120], ["D_7", 240], ["CS_7", 120], ["C_7", 240], ["GS_6", 120], ["C_7", 180], ["B_6", 60], ["AS_6", 120], ["FS_6", 240], ["G_6", 120], ["E_6", 255], ["E_6", 255], ["E_6", 90], ["G_6", 120], ["B_6", 240], ["G_6", 120], ["B_6", 240], ["G_6", 120], ["C_7", 240], ["B_6", 120], ["AS_6", 240], ["FS_6", 120], ["G_6", 180], ["B_6", 60], ["AS_6", 120], ["AS_5", 240], ["B_5", 120], ["B_6", 255], ["B_6", 255],["B_6", 90], ["G_6", 120], ["B_6", 240], ["G_6", 120], ["B_6", 240], ["G_6", 120], ["D_7", 240], ["CS_7", 120], ["C_7", 240], ["GS_6", 120], ["C_7", 180], ["B_6", 60], ["AS_6", 120], ["FS_6", 240], ["G_6", 120], ["E_6", 255], ["E_6", 255], ["E_6", 90]]
# 	harry_tempo = 4
# 	print("Playing Harry Potter Theme")
# 	play_song(harry_midi, harry_tempo)
# 	buzzer_off()

