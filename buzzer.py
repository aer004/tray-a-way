import tray
import time

harry_midi = [[B_5, 120], [E_6, 180], [G_6, 60], [FS_6, 120], [E_6, 240], [B_6, 120], [A_6, 255], [A_6, 105], [FS_6, 255], [FS_6, 105], [E_6, 180], [G_6, 60], [FS_6, 120], [D_6, 240], [F_6, 120], [B_5, 255], [B_5, 255], [B_5, 210], [E_6, 180], [G_6, 60], [FS_6, 120], [E_6, 240], [B_6, 120], [D_7, 240], [CS_7, 120], [C_7, 240], [GS_6, 120], [C_7, 180], [B_6, 60], [AS_6, 120], [FS_6, 240], [G_6, 120], [E_6, 255], [E_6, 255], [E_6, 90], [G_6, 120], [B_6, 240], [G_6, 120], [B_6, 240], [G_6, 120], [C_7, 240], [B_6, 120], [AS_6, 240], [FS_6, 120], [G_6, 180], [B_6, 60], [AS_6, 120], [AS_5, 240], [B_5, 120], [B_6, 255], [B_6, 255],[B_6, 90], [G_6, 120], [B_6, 240], [G_6, 120], [B_6, 240], [G_6, 120], [D_7, 240], [CS_7, 120], [C_7, 240], [GS_6, 120], [C_7, 180], [B_6, 60], [AS_6, 120], [FS_6, 240], [G_6, 120], [E_6, 255], [E_6, 255], [E_6, 90]]
harry_tempo = 4

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



