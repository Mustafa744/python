import time
import mouse
text=open("D:/mouse1.txt","r")
def Mouse_control(line) :
    for i in range(len(line)):
        if line[i]==",":
            x=line[1:i]
            y=line[i+2:-3]
            state=line[len(line)-2]
    print "x=",x,"y=",y,"state =",state,"\n"        
    if mouse.is_pressed (button="middle"):
        exit()
    mouse.move(int(x), int(y), absolute=True, duration=0)
    if state =="1":
        mouse.press(button='left')
        print "\a"
    elif state=="0" :
       mouse.release(button='left')
    time.sleep(0.01)

for line in text:
    Mouse_control(line)
