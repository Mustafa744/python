import time
import cv2
import numpy as np
import os
import urllib.request
url = "http://192.168.1.3:8080/shot.jpg"
drawing=1

last_move = ""
successful = 1
factA = 0.75
factE = 0.75
out = fourcc = 0

state = ""
ang = 0
x_offset = 120
y_offset = 160
leftmost=(0,0)
rightmost=(319,0)
topmost=(100,0)
bottommost=(100,240)
kernel = np.ones((3, 3), np.uint8)

low_black = np.array([0, 0, 0])
high_black = np.array([75, 75, 75])

#low_green = np.array([25, 52, 72])
#high_green = np.array([102, 255, 255])

low_green = np.array([161, 155, 84])
high_green = np.array([179, 255, 255])


def draw_bar(position,length):
    bar=[]
    for i in range(length):
        bar.append("_")
    os.system('cls')
    print("\n")
    bar[int(position)-1]="O"
    for char in bar:
        print(char,end="")
    bar[int(position)-1]="_"


def correct_black(contours):
    cnotours_blk = contours
    length = len(contours_blk)
    if len(contours_blk) != 0:
        if length == 1:
            selection = 0

        else:
            suspects = []
            for index, possible in enumerate(contours_blk):
                bottommost = tuple(possible[possible[:, :, 1].argmax()][0])
                suspects.append([bottommost[1], index])
            suspects.sort()
            selection = suspects[-1][1]
        #cv2.drawContours(blank_image, contours_blk, selection, (255, 255, 255), 10)
        cnt = contours_blk[selection]

        return cnt


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def motor(speed, steering):
    if steering == 0:
        port1 = speed
        port2 = speed
    elif steering > 0:
        steering = 100 - steering
        port1 = speed * steering / 100
        port2 = speed
    elif steering < 0:
        steering = steering * -1
        steering = 100 - steering
        port1 = speed
        port2 = speed * steering / 100
    return int(port1), int(port2)




def correct_green(points):
    correct_points = []
    if points is not None:
        for point in points:
            # point is on the left
            if abs(point[0] - leftmost[0]) < abs(point[0] - rightmost[0]):
                if leftmost[1] < point[1]:
                    correct_points.append(point)
            else:
                if rightmost[1] < point[1]:
                    correct_points.append(point)
    for point in correct_points:
        cv2.circle(blank_image, point, 10, (200, 0, 250), -1)
    return correct_points


def check_green():
    points = []
    hsv_frame = cv2.cvtColor(image_raw, cv2.COLOR_BGR2HSV)
    greenmark = cv2.inRange(hsv_frame, low_green, high_green)
    kernel = np.ones((3, 3), np.uint8)
    greenmark = cv2.erode(greenmark, kernel, iterations=3)
    greenmark = cv2.dilate(greenmark, kernel, iterations=9)
    __ ,contours_green, hierarchy_green = cv2.findContours(greenmark, cv2.RETR_TREE,
                                                                  cv2.CHAIN_APPROX_SIMPLE)


    if len(contours_green) > 2:
        contours_green = [contours_green[0], contours_green[1]]
    for cnt_green in contours_green:
        M = cv2.moments(cnt_green)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        points.append((cx, cy))
    new_points = correct_green(points)

    return len(new_points), new_points


count = 0
start = time.time()
center = 160
ang=0


imgResp = urllib.request.urlopen(url)
imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
image_raw = cv2.imdecode(imgNp, -1)
image_raw=image_raw[1:-1,1:-1]

while successful:
    # black blank image
    blank_image = np.zeros(shape=[320, 320, 3], dtype=np.uint8)
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    image_raw = cv2.imdecode(imgNp, -1)




    count = count + 1
    image = np.array(image_raw)

    #image = cv2.resize(image, None, fx=1.333, fy=1, interpolation=cv2.INTER_CUBIC)

    Blackline = cv2.inRange(image, low_black, high_black)
    Blackline = cv2.erode(Blackline, kernel, iterations=2)
    Blackline = cv2.dilate(Blackline, kernel, iterations=3)
    __, contours_blk, hierarchy_blk = cv2.findContours(Blackline, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    line = correct_black(contours_blk)
    if line is not None:

        rect = cv2.minAreaRect(line)
        (x_min, y_min), (w_min, h_min), ang = rect
        M = cv2.moments(line)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])




        leftmost = tuple(line[line[:, :, 0].argmin()][0])
        rightmost = tuple(line[line[:, :, 0].argmax()][0])
        topmost = tuple(line[line[:, :, 1].argmin()][0])
        bottommost = tuple(line[line[:, :, 1].argmax()][0])

        width = int(abs(leftmost[0] - rightmost[0]))
        height = int(abs(topmost[1] - bottommost[1]))
        vertical_error = int(topmost[1])

        ang = int(ang)
        if ang < -45:
            ang = 90 + ang
        if w_min < h_min and ang > 0:
            ang = (90 - ang) * -1
        if w_min > h_min and ang < 0:
            ang = 90 + ang
        else:
            pass
        error = int(x_min) - x_offset

        if width >= x_offset * 2 - 3 or height >= y_offset * 2 - 3:
            length_green = check_green()
            if length_green[0] != 0:
                print("possible intersection")
                if length_green[0] ==2:
                    print("turn arround")
                    ang=0
                    error=-250
                else :
                    green_square=length_green[1][0]
                    if green_square[0]>cx :
                        print("intersection right")
                        ang=0
                        error=190
                    elif green_square[0]<cx :
                        print("intersection left")
                        ang = 0
                        error = -190
            else:
                length_green=None
        if topmost[1]>30:
            #print("angle detected " + state)
            if error < -20:
                state = "sharp-left"
                last_move = "l"
                ang=0
                error=-190
            elif error > 20:
                state = "sharp-right"
                last_move = "r"
                ang = 0
                error = 190
            else:
                state = last_move



        r, l = motor(100, error * factA + ang*factE)

        #print(l, "   ", r,"  ", ang,"  ",error)
        draw_bar(int(x_min/5),50)



#fps = count/(finish - start)
#print("fps=  ", fps)
exit()
