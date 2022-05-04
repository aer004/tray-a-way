import RPi.GPIO as GPIO
import pigpio
import time

# Buzzer Constants
BUZZ_FREQ = 4000
HALF_DUTY = 500000
ZERO_DUTY = 0
PWM_PIN = 13

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

buzzer_setup()
buzzer_on()
time.sleep(5)
buzzer_off()

