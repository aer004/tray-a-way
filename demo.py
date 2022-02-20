import tray
import time

while (True == 1):
	tray.buzzer_on()
	print("Buzzer on")
	time.sleep(5)
	tray.buzzer_off()
	print("Buzzer off")
	time.sleep(5)

