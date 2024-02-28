import sys
import cv2
import numpy as np
import math
import random

img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
codels = [0, 1, 2, 3, 4, 5, 6, 7]



#Making an image from random distribution
def random_img(edgepercodel):
    random_img = np.zeros(shape=[504, 378, 3], dtype=np.uint8)
    for i in edgepercodel:
        p = edgepercodel.index(i)
        for x in range(0, 378):
            for y in range(p*63, (p+1) * 63):
                if(random.randint(0, 378*63) < i):
                    random_img[y, x] = 255
    cv2.imshow("random", random_img)
    cv2.waitKey(0)

#Making an image by putting pixels at top left
def condensed_img_top(edgepercodel):
    condensed_img = np.zeros(shape=[504, 378, 3], dtype=np.uint8)
    for i in edgepercodel:
        p = edgepercodel.index(i)
        condensed_img[p*63:p*63 + math.ceil(i / 378), 0:i] = 255
    cv2.imshow("condensed top", condensed_img)
    cv2.waitKey(0)

#Making an image by putting pixels at top left
def condensed_img_left(edgepercodel):
    condensed_img = np.zeros(shape=[504, 378, 3], dtype=np.uint8)
    for i in edgepercodel:
        height = i
        if height > 63:
            height = 63
        p = edgepercodel.index(i)
        condensed_img[p*63:p*63 + height, 0:math.ceil(i / 63)] = 255
    cv2.imshow("condensed left", condensed_img)
    cv2.waitKey(0)

#Making an image by averaging out the total color, weighted
def average_img(edgepercodel):
    average_img = np.zeros(shape=[504, 378, 3], dtype=np.uint8)
    for i in edgepercodel:
        p = edgepercodel.index(i)
        average_img[p*63:(p+1)* 63, 0:378] = round(edgepercodel[p] * 1275 / (378*63))
    cv2.imshow("average", average_img)
    cv2.waitKey(0)

#Making an image by averaging out the total color
def true_average_img(edgepercodel):
    average_img = np.zeros(shape=[504, 378, 3], dtype=np.uint8)
    for i in edgepercodel:
        p = edgepercodel.index(i)
        average_img[p*63:(p+1)* 63, 0:378] = round(edgepercodel[p] / (378*63))
    cv2.imshow("true average", average_img)
    cv2.waitKey(0)

#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def difference_code(prev_codel, current_codel, threshold):
    if current_codel < prev_codel - threshold:
        return 0
    elif current_codel > prev_codel + threshold:
        return 2
    else:
        return 1

#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def left_values(codels):
    leftmost_codel_list = [378,378,378,378,378,378,378,378]
    for z in range (0,8):
        for x in range(0,378):
            for y in range(0, 63):
                #checks to see if the current pixel is not black
                if(codels[z][y,x] != 0):
                    leftmost_codel_list[z] = x

                    break
            else:
                continue
                
            break

    #defines a threshold for comparison between codels, based on a fraction of the total number of pixels in the codel.
    return(leftmost_codel_list)

def right_values(codels):
    rightmost_codel_list = [378,378,378,378,378,378,378,378]
    for z in range (0,8):
        for x in range(0, 378):
            for y in range(0, 63):
                rx = 377 - x
                if(codels[z][y,rx] != 0):
                    rightmost_codel_list[z] = rx
                    break
            else:
                continue
                
            break

    #defines a threshold for comparison between codels, based on a fraction of the total number of pixels in the codel.
    return(rightmost_codel_list)

def edge_values(codels):
    edgepercodel = [0, 0, 0, 0, 0, 0, 0, 0] 
    #displays codels one at a time
    for z in range (0,8):
        #cv2.imshow("codel " + str(z), codels[z])
        #cv2.waitKey(0)
        q = 0
        for y in range(0,378):
            for x in range(0, 63):
                #checks to see if the current pixel is not black
                if(codels[z][x,y] != 0):
                    print(str(x) + ", " + str(y))
                    q += 1
        edgepercodel[z] = q

    return edgepercodel

def print_codes(left_list, total_list, right_list, threshold_left, threshold_total, threshold_right):
    for i in range(1, len(total_list)):
        print(str(difference_code(left_list[i - 1], left_list[i], threshold_left)), str(difference_code(total_list[i - 1], total_list[i], threshold_total)), str(difference_code(right_list[i - 1], right_list[i], threshold_right)))


#performs canny edge detection on image and displays result 
resize_img = cv2.resize(img, (378, 504))
cv2.imshow("original", resize_img)
cv2.waitKey(0)
edges = cv2.Canny(resize_img, threshold1 = 100, threshold2 = 200)
cv2.imshow("canny", edges)
cv2.waitKey(0)
cv2.imwrite("output.jpg", edges)

#cuts image into codels
i = 0
while i < 8:
    codels.insert(i, edges[63*i:63*(i+1), 0:378])
    i += 1

edgepercodel = edge_values(codels)
left_values = left_values(codels)
right_values = right_values(codels)

random_img(edgepercodel)
condensed_img_top(edgepercodel)
condensed_img_left(edgepercodel)
average_img(edgepercodel)
true_average_img(edgepercodel)

print_codes(left_values, edgepercodel, right_values, 5, (378 * 63) / 100, 5)

