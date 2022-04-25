/* 
Issue: https://github.com/rb2468/tray-a-way/issues/72
 
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
- changes armed vs. unarmed (true or false)
- if disarmed:
- do nothing if there are weight changes

One thread constantly checking the state of the LED
- 3 states:
- armed (white)
- disarmed (green)
- failure to scan (red)
*/
