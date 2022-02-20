import pigpio
import time

pi = pigpio.pi()

def buzzer_on():
	pi.hardware_PWM(13, 4000, 500000)

##def buzzer_off():

<<<<<<< HEAD
##def play_tone(tone):
=======
def play_tone(tone):

def readNFC():
  # when the NFC scans, notify that it reads 
  
def greenLED():
  # turn LED green if NFC was read successfully

def redLED():
  # else, turn LED red to notify user that the NFC was not read 

def measureWeight():
 
def detectWeightChange():
>>>>>>> 3f7f32733dfdeea9bd98f8a02baadeb1967e2507
