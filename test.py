import RPi.GPIO as GPIO
import time

# LED Pins
RED_PIN = 19 
GREEN_PIN = 12
BLUE_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
pwm_red = GPIO.PWM(RED_PIN, 50) 

def led_setup():
	## Red LED 
	pwm_red.start(50) # duty cycle starting at 0

	## Green LED
	GPIO.setup(GREEN_PIN, GPIO.OUT)
	pwm_green = GPIO.PWM(GREEN_PIN, 100)
	pwm_green.start(0)

	## Blue LED
	GPIO.setup(BLUE_PIN, GPIO.OUT)
	pwm_blue = GPIO.PWM(BLUE_PIN, 100)
	pwm_blue.start(0)

# Failure to Scan Tag
def red_led():
	pwm_red.ChangeDutyCycle(50)
    

# ARMED = False, (Disarmed) -- Let the user safely use the tray
def green_led():
	GPIO.output(RED_PIN, GPIO.LOW)
	GPIO.output(BLUE_PIN, GPIO.LOW)
	GPIO.output(GREEN_PIN, GPIO.HIGH)
    

# ARMED = True, Working Tray
def white_led():
	GPIO.output(BLUE_PIN, GPIO.HIGH)
	GPIO.output(GREEN_PIN, GPIO.HIGH)
	GPIO.output(RED_PIN, GPIO.HIGH)

def led_off():
	GPIO.output(RED_PIN, GPIO.LOW)
	GPIO.output(GREEN_PIN, GPIO.LOW)
	GPIO.output(BLUE_PIN, GPIO.LOW)

led_setup()
print("white")
#red_led()
time.sleep(30)
red_pwm.ChangeDutyCycle(0)
#print("red")
#red_led()
#time.sleep(5)
#print("green")
#green_led()
#time.sleep(5)
#led_off()
