"""
Issue: https://github.com/rb2468/tray-a-way/issues/72
 -- import libraries
 -- define an empty function for each task
 
What we need:
Continuously monitor if anything scanned
Continuously monitor any weight changes
- have an initial weight to detect changes
- document the weight change (time)
- silent alarm/loud alarm

Infinite loop

check if armed (true or false depending on scan)
if armed: detect the weight
if a specific amount of weight was changed then document it, and set off an alarm (true or false)
else: no change
Continuously monitor if anything scanned
- changes armed vs. disarmed (true or false)
- if disarmed:
- do nothing if there are weight changes

One thread constantly checking the state of the LED
- 3 states:
- armed (white)
- disarmed (green)
- failure to scan (red)
"""

import pigpio
import time
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from py532lib.mifare import *

# Constants
ARMED = True
"""
ARMED = True is the default since the Tray-a-way should be tracking for weight changes

When ARMED = True, this means that  
"""

# Thread for continuously monitoring the NFC reader

# Thread for checking if it is armed 
