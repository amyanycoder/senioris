import sys
import cv2
import numpy as np
import math
import random
from collections import deque
from fsm import fsmRunner

img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
codel_height = 200



#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def difference_code(prev_codel, current_codel, threshold):
    if current_codel < prev_codel - threshold:
        return 0
    elif current_codel > prev_codel + threshold:
        return 2
    else:
        return 1


#assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same , or less edges than the previous codel.
def left_valuer(codels_list, width):
    leftmost_codel_list = []
    i = 0
    while i < len(codels_list):
        leftmost_codel_list.append(width)
        i += 1

    for z in range (0, len(codels_list)):
        for x in range(0,width):
            for y in range(0, codel_height):
                #checks to see if the current pixel is not black
                if(codels_list[z][y,x] != 0):
                    leftmost_codel_list[z] = width - x

                    break
            else:
                continue
                
            break


    #defines a threshold for comparison between codels, based on a fraction of the total number of pixels in the codel.
    return(leftmost_codel_list)

def right_valuer(codels_list, width):
    rightmost_codel_list = []
    i = 0
    while i < len(codels_list):
        rightmost_codel_list.append(0)
        i += 1

    for z in range (0, len(codels_list)):
        for x in range(0,width):
            for y in range(0, codel_height):
                rx = (width - 1) - x
                if(codels_list[z][y,rx] != 0):
                    rightmost_codel_list[z] = rx
                    break
            else:
                continue
                
            break
    #defines a threshold for comparison between codels, based on a fraction of the total number of pixels in the codel.
    return(rightmost_codel_list)
    

#counts the number of edges (non-black pixels) in each codel
def edge_valuer(codels_list, width):
    edgepercodel = [] 
    #adds up edges, one codel at a time.
    for i in range (0, len(codels_list)):
        q = 0
        for y in range(0, width):
            for x in range(0, codel_height):
                #checks to see if the current pixel is not black.  If so, add it to q, the pixel counter
                if(codels_list[i][x,y] != 0):
                    q += 1
        edgepercodel.append(q)

    return edgepercodel

def assembleCodesDeque(left_list, total_list, right_list, threshold_left, threshold_total, threshold_right):
    codes_deque = deque()
    for i in range(1, len(total_list)):
        #A two value tuple:  The first value is the three digits of the code as a tuple.  The second value is the number the code was added.
        codes_deque.append(((difference_code(left_list[i - 1], left_list[i], threshold_left), difference_code(total_list[i - 1], total_list[i], threshold_total), 
                            difference_code(right_list[i - 1], right_list[i], threshold_right)), i - 1))
    
    return codes_deque

def main():
    default_img = "barbiecrop.png"
    if __name__ == "__main__":
        if(len(sys.argv) < 2):
            print("No image specified.  Using default image file.")
            img = cv2.imread(default_img, cv2.IMREAD_ANYCOLOR)
        elif(len(sys.argv) == 2):
            img = cv2.imread(sys.argv[1], cv2.IMREAD_ANYCOLOR)
        else:
            print("Too many arguments.  Using default image file.")
            img = cv2.imread(default_img, cv2.IMREAD_ANYCOLOR)

    height, width, channels = img.shape

    #performs canny edge detection on image and displays result 
    edges = cv2.Canny(img, threshold1 = 100, threshold2 = 200)
    cv2.imshow("canny", edges)
    cv2.waitKey(0)

    #cuts image into codels
    codels_list = []
    codels = int(height / codel_height)
    i = 0
    while i < codels:
        codels_list.insert(i, edges[codel_height * i:codel_height * (i+1), 0:width])
        cv2.imshow("latest", codels_list[i])
        cv2.waitKey(0)
        i += 1

    #creates array of left, middle, and right digits
    edgepercodel = edge_valuer(codels_list, width)
    left_values = left_valuer(codels_list, width)
    right_values = right_valuer(codels_list, width)

    #combines digits into three digit codes
    codes_deque = assembleCodesDeque(left_values, edgepercodel, right_values, width * 0.1, (width * codel_height) / 100, width * 0.1)

    print(codes_deque)
    final_img = fsmRunner(codes_deque, img, sys.argv[1])
    cv2.imshow("Final Image", final_img)
    cv2.waitKey(0)
    cv2.imwrite("test.jpg", final_img)


if __name__ == "__main__":
    main()