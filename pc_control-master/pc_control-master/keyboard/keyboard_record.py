"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""
import time
import sys
sys.path.append('..')
import keyboard

def Keyboard_record(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
	# '\r' and end='' overwrites the previous line.
	# ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    if line:
        print(line)
    
keyboard.hook(Keyboard_record)
while 1:
    
    time.sleep(0.01)
