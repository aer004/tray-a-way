import tray
import time

harry_midi = [[988, 0.48], [1319, 0.72], [1568, 0.24], [1480, 0.48], [1319, 0.96], [1976, 0.48], [1760, 1.44]]
for i in range(len(harry_midi)):
	j = 0
	tray.play_tone(harry_midi[i][j])
	j += 1
	time.sleep(harry_midi[i][j])
tray.buzzer_off()
