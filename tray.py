import pigpio
import time

pi = pigpio.pi()
frequency_chart = {"C_5": 523, "CS_5": 554, "D_5": 587, "DS_5": 622, "E_5": 659, "F_5": 698, "FS_5": 740, "G_5": 784, "GS_5": 831, "A_5": 880, "AS_5": 932, "B_5": 988, "C_6": 1047, "CS_6": 1109, "D_6": 1175, "DS_6": 1245, "E_6": 1319, "F_6": 1397, "FS_6": 1480, "G_6": 1568, "GS_6": 1661, "A_6": 1760, "AS_6": 1865, "B_6": 1976, "C_7": 2093, "CS_7": 2217, "D_7": 2349, "DS_7": 2489, "E_7": 2637, "F_7": 2794, "FS_7": 2960, "G_7": 3136, "GS_7": 3322, "A_7": 3520, "AS_7": 3729, "B_7": 3951}

def buzzer_on():
	"Turns buzzer on"
	pi.hardware_PWM(13, 4000, 500000)

def buzzer_off():
	"Turns buzzer off"
	pi.hardware_PWM(13, 4000, 0)

def play_tone(tone):
	"Plays buzzer at certain tone, which is give in frequency"
	pi.hardware_PWM(13, tone, 500000)

def play_song(song, tempo):
	"Input is a list with a list for every note. The zeroth index of the inner lists (song[i][0]) are keys for the frequency dictionary, which have values in Hz for each midi note. Then, the first index of the inner lists (song[i][1]) is the amount of durations the note should be played. To change that to seconds, the durations have to be multipled by the tempo, which is in milliseconds, so then the resulting value has to be divided by 1000."
	for i in range(len(song)): #go through length of input list
		play_tone(frequency_chart[song[i][0]]) #play tone from frequency dictionary
		time_seconds = (song[i][1] * tempo)/1000
		time.sleep(time_seconds) #let tone play for given time

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
	#Detects initial weight on load cells when tray is first turned on for reference
	pass

def detectWeightChange():
	#If weight is removed load cell, function will send message to user
	pass
