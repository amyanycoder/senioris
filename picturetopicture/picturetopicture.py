import sys
import cv2
import numpy as np
import math
import random
from collections import deque
from fsm import fsmRunner

img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
codel_height = 200

'''
difference_code

Assigns the number 2, 1, or 0, depending if the current codel has significantly greater, about the same, or less edges than the previous codel.

Parameters:
prev_codel:     int, the previous value in the sequence
current_codel:  int, the current value in the sequence
threshold:      int, determines the margin in which prev_codel and current_codel are considered equal.

Returns:  The integer values  2, 1, or 0.
'''
def difference_code(prev_codel, current_codel, threshold):
    if current_codel < prev_codel - threshold:
        return 0
    elif current_codel > prev_codel + threshold:
        return 2
    else:
        return 1

'''
left_valuer

Runs through a list of codels and finds the leftmost pixel in each one.

Parameters:
codels_list:    List, list of the codels in order
width:          int, the width of the image

Returns:
A list of the leftmost pixel in each codel, by x-position.
'''
def left_valuer(codels_list, width):
    leftmost_codel_list = []
    i = 0
    #creates a list that is (number of codels) long, each value being the width of the image.
    while i < len(codels_list):
        leftmost_codel_list.append(width)
        i += 1

    #checks all pixels in all codels to find the leftmost pixel in each
    for z in range (0, len(codels_list)):
        #checks all pixels in codel
        for x in range(0,width):
            for y in range(0, codel_height):
                #checks to see if the current pixel is not black
                if(codels_list[z][y,x] != 0):
                    leftmost_codel_list[z] = width - x

                    break
            else:
                continue
                
            break

    return(leftmost_codel_list)

'''
right_valuer

Runs through a list of codels and finds the rightmost pixel in each one

Parameters:
codels_list:    List, list of the codels in order
width:          int, the width of the image

Returns:
A list of the rightmost pixel in each codel, by x-position.
'''
def right_valuer(codels_list, width):
    rightmost_codel_list = []
    i = 0
    #creates a list that is (number of codels) long, each value being 0.
    while i < len(codels_list):
        rightmost_codel_list.append(0)
        i += 1

    #checks all pixels in all codels to find the leftmost pixel in each
    for z in range (0, len(codels_list)):
        #checks all pixels in codel
        for x in range(0,width):
            for y in range(0, codel_height):
                rx = (width - 1) - x
                #checks to see if the current pixel is not black
                if(codels_list[z][y,rx] != 0):
                    rightmost_codel_list[z] = rx
                    break
            else:
                continue
                
            break
    #defines a threshold for comparison between codels, based on a fraction of the total number of pixels in the codel.
    return(rightmost_codel_list) 

'''
edge_valuer

Counts the number of edges (non-black pixels) in each codel and returns this as a list.

Parameters:
codels_list:    List, list of the codels in order
width:          int, the width of the image

Returns:
A list of of the number of edge pixels in each image
'''
def edge_valuer(codels_list, width):
    print("Analyzing codels...")
    edgepercodel = [] 
    #adds up edges, one codel at a time.
    for i in range (0, len(codels_list)):
        print("Analyzing codel " + str(i + 1) + " of " + str(len(codels_list)) + "...")
        q = 0
        for y in range(0, width):
            for x in range(0, codel_height):
                #checks to see if the current pixel is not black.  If so, add it to q, the pixel counter
                if(codels_list[i][x,y] != 0):
                    q += 1
        edgepercodel.append(q)

    return edgepercodel

'''
assembleCodesDeque

Takes the leftmost edge values, rightmost edge values, and total edge values and assembles a deque of three digit codes based on this info.

Parameters:
left_list:          List, the list of the leftmost pixel in each codel, by x-position
total_list:         List, the list of of the number of edge pixels in each image
right_list:         List, the list of the rightmost pixel in each codel, by x-position
threshold_left:     int, the threshold denoting equality for the left values
threshold_total:    int, the threshold denoting equality for the total values
threshold_right:    int, the threshold denoting equality for the right values

Returns:            A deque of base-3, three digit codes symbolizing the differences in left position, right position, and total amount of edges between all codels in the image.
'''
def assembleCodesDeque(left_list, total_list, right_list, threshold_left, threshold_total, threshold_right):
    codes_deque = deque()
    for i in range(1, len(total_list)):
        #A two value tuple:  The first value is the three digits of the code as a tuple.  The second value is the number the code was added.
        codes_deque.append(((difference_code(left_list[i - 1], left_list[i], threshold_left), difference_code(total_list[i - 1], total_list[i], threshold_total), 
                            difference_code(right_list[i - 1], right_list[i], threshold_right)), i - 1))
    
    return codes_deque
'''
main

The main function: takes a command line file for the image and runs through the process of analyzing codels, generating codes, and running functions on the image.
'''
def main():
    file_path = "examples/girl.jpg"
    verbose = False

    #reads image file from command line arg
    if __name__ == "__main__":
        #uses a default image if none is specified
        if(len(sys.argv) < 2):
            print("No image specified.  Using default image file.")
            img = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        elif(len(sys.argv) == 2):
            #activates verbose mode if -v flag used
            if(sys.argv[1] == "-v"):
                verbose = True
                print("No image specified.  Using default image file.")
                img = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
            #uses arg file if one is specified
            else:
                img = cv2.imread(sys.argv[1], cv2.IMREAD_ANYCOLOR)

                file_path = sys.argv[1]
        #allows for the specification of a verbose mode
        elif(len(sys.argv) == 3):
            #if there is a "-v" argument, activates verbose mode
            if(sys.argv[2] == "-v"):
                verbose = True
            #if the second argument is not "-v, ignores"
            else:
                print("Incorrect second parameter.  Did you mean -v?")
                
            img = cv2.imread(sys.argv[1], cv2.IMREAD_ANYCOLOR)
            file_path = sys.argv[1]
        #if more than 2 arguments, defaults to the default file
        else:
            print("Too many arguments.  Using default image file.")
            img = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)

    #takes height, width, and channel values from the input image.  If the image is greyscale, converts the image to RGB
    try:
        height, width, channels = img.shape
    #Will fail the try block if the image is grayscale, or the file path itself is bad
    except:
        #Assuming the image is grayscale, converts to RGB format
        try:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            height, width, channels = img.shape
        #uses default image if the image argument is bad
        except:
            print("Bad file path.  Using default image.")
            file_path = "girl.jpg"
            img = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
            height, width, channels = img.shape

    #performs canny edge detection on image and displays result 
    edges = cv2.Canny(img, threshold1 = 200, threshold2 = 250)
    if(verbose == True):
        cv2.imshow("canny", edges)
        cv2.waitKey(0)

    #cuts image into codels
    codels_list = []
    codels = int(height / codel_height)
    i = 0
    while i < codels:
        codels_list.insert(i, edges[codel_height * i:codel_height * (i+1), 0:width])
        #if verbose mode is on, displays each codel as it is cut from the original image.
        if(verbose == True):
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
    #calls fsm to begin the process of interpeting the deque of codes and creating the output image
    final_img = fsmRunner(codes_deque, img, file_path)
    #displays the final code, if in verbose mode
    if(verbose == True):
        cv2.imshow("Final Image", final_img)
        cv2.waitKey(0)
    #writes the output image to output.jpg
    cv2.imwrite("output.jpg", final_img)


if __name__ == "__main__":
    main()