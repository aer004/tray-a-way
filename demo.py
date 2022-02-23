import tray
import time

print("Testing buzzer_on function...")
tray.buzzer_on()
print("Buzzer on")
time.sleep(3)
tray.buzzer_off()
print("Buzzer off")

tray.play_tone(1000)
print("Playing buzzer tone at frequency 1000")
time.sleep(3)
tray.play_tone(3000)
print("Playing buzzer tone at frequency 3000")

