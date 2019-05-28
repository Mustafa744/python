import time
import keyboard
time.sleep(3)
text=open("D:/mouse1.txt","r")
def Keyboard_control(line) :
    for i in range(len(line)) :
        if line[i]==" ":
            key=line[:i]
            state=line[i+1:]
    print "key=",key,"state =",state,"\n"

    if "down"in state :
        keyboard.press(key)
        time.sleep(0.01)
    elif "up" in state :
        keyboard.release(key)
        time.sleep(0.01)
for line in text:
    Keyboard_control(line)
    

