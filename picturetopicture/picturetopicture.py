import sys
import cv2
import numpy as np
import math
import random
from collections import deque
from fsm import fsmRunner

img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
codels = [0, 1, 2, 3, 4, 5, 6, 7]


#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def difference_code(prev_codel, current_codel, threshold):
    if current_codel < prev_codel - threshold:
        return 0
    elif current_codel > prev_codel + threshold:
        return 2
    else:
        return 1

#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def left_valuer(codels):
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

def right_valuer(codels):
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

def edge_valuer(codels):
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
                    q += 1
        edgepercodel[z] = q

    return edgepercodel

def assembleCodesDeque(left_list, total_list, right_list, threshold_left, threshold_total, threshold_right):
    codes_deque = deque()
    for i in range(1, len(total_list)):
        #appends a code in the form of a tuple to the end of the deque
        codes_deque.append((difference_code(left_list[i - 1], left_list[i], threshold_left), difference_code(total_list[i - 1], total_list[i], threshold_total), 
                            difference_code(right_list[i - 1], right_list[i], threshold_right)))
    
    return codes_deque

def main():
    #performs canny edge detection on image and displays result 
    resize_img = cv2.resize(img, (378, 504))
    edges = cv2.Canny(resize_img, threshold1 = 100, threshold2 = 200)

    #cuts image into codels
    i = 0
    while i < 8:
        codels.insert(i, edges[63*i:63*(i+1), 0:378])
        i += 1

    edgepercodel = edge_valuer(codels)
    left_values = left_valuer(codels)
    right_values = right_valuer(codels)


    codes_deque = assembleCodesDeque(left_values, edgepercodel, right_values, 5, (378 * 63) / 100, 5)

    print(codes_deque)
    fsmRunner(codes_deque)



if __name__ == "__main__":
    main()