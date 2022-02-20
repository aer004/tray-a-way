import pigpio
import time
import RPi.GPIO as GPIO

pi = pigpio.pi()

def buzzer_on():
	"Turns buzzer on"
	pi.hardware_PWM(13, 5000, 500000)

def buzzer_off():
	"Turns buzzer off"
	pi.hardware_PWM(13, 5000, 0)

def play_tone(tone):
	"Plays buzzer at certain tone"
	pass

def readNFC():
	#when the NFC scans, notify that it reads
	pass

def greenLED():
	#turn LED green if NFC was read successfully
	pass

def redLED():
	#else, turn LED red to notify user that the NFC was not read
	pass

def measureWeight():
	pass

def detectWeightChange():
	pass
