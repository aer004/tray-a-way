import tray
import time

"""
print("buzzer")
tray.buzzer_setup()
tray.buzzer_on()
time.sleep(2)
tray.buzzer_off()
print("buzzer off")
"""

tray.buzzer_setup()
tray.buzzer_off()

tray.led_setup()
print("red")
tray.red_led()
time.sleep(2)
tray.led_off()
time.sleep(2)
print("green")
tray.green_led()
time.sleep(2)
tray.led_off()
time.sleep(2)
print("white")
tray.white_led()
time.sleep(2)
tray.led_off()

"""
tray.load_cell_setup()
while True:
	tray.measure_weight()
	time.sleep(2)
"""

