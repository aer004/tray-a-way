import pigpio
import time

pi = pigpio.pi()

def buzzer_on():
	pi.hardware_PWM(13, 4000, 500000)

##def buzzer_off():

##def play_tone(tone):
