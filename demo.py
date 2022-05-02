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

try:
	tray.nfc_setup()
	print("Testing read_nfc function...")
	print("Hold a tag near the NFC reader")
	print("Reading tag in 1 second...")
	time.sleep(1)

	print("Please scan tag in 5 seconds")
	tray.read_nfc()
except:
	print("Reading the NFC module did not work")

try:
	tray.load_cell_setup()
	print("Load Cell has been calibrated")
	time.sleep(3)
	
	print("Current weight is: ")
	tray.measure_weight()
except:
	print("Load Cells did not function properly")
