import tray
import time

try:
	tray.buzzer_setup()
	print("Testing buzzer_on function...")
	tray.buzzer_on()
	print("Buzzer on")
	time.sleep(3)
	tray.buzzer_off()
	print("Buzzer off")
	time.sleep(3)

	tray.play_tone(1000)
	print("Playing buzzer tone at frequency 1000")
	time.sleep(3)
	tray.play_tone(3000)
	print("Playing buzzer tone at frequency 3000")
	time.sleep(3)

except:
	print("Buzzer test did not function")

try:
	tray.play_harry()
except:
	print("Playing Harry Potter did not work")
