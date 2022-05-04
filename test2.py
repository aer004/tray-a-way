import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
# first arg is pin number, second is frequency in Hz
green_out = GPIO.output(12, GPIO.HIGH)
time.sleep(2)
green_out = GPIO.output(12, GPIO.LOW)
# argument is duty cycle, out of 100 parts

# observe output for 60 seconds
time.sleep(2)
green_out = GPIO.output(12, GPIO.HIGH)
