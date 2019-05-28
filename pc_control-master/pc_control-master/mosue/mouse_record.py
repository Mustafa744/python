import time
import mouse
text=open("D:/mouse1.txt","w")
def record_mouse():
    status=""
    if mouse.is_pressed(button="left"):
        status= "1"
    else :
        status = "0"
    position =str(mouse.get_position())   
    text.write(position+status+"\n")
    print (position+status+"\n")

    time.sleep(0.01)
while 1 :
    record_mouse()
