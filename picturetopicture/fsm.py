#from statemachine import StateMachine, State
from collections import deque
import cv2
import manip

def fsmRunner(codes_deque, img):
    region = 0
    state = 0
    prev_state = -1
    subimage_deque = deque()
    merge_img = img

    '''
    Legend:
    [Integer] [State]
    0          Start
    1          Code
    2          Statement
    3          Python
    4          Random
    5          Sort
    6          JPEG
    7          Threshold
    8          Functional Sort
    9          Fractal
    10         Print
    11         Canny
    -1         End

    '''

    init_dict = {
        (0,0,0): 1,
        (0,0,1): 1,
        (0,0,2): 1,
        (0,1,0): 2,
        (0,1,1): 2,
        (0,1,2): 2,
        (0,2,0): 3,
        (0,2,1): 3,
        (0,2,2): 3,
        (1,0,0): 6,
        (1,0,1): 6,
        (1,0,2): 6,
        (1,1,0): 7,
        (1,1,1): 8,
        (1,1,2): 11,
        (1,2,0): 10,
        (1,2,1): 10,
        (1,2,2): 10,
        (2,0,0): 4,
        (2,0,1): 5,
        (2,0,2): 5,
        (2,1,0): 9,
        (2,1,1): 9,
        (2,1,2): 9,
        (2,2,0): 9,
        (2,2,1): 9,
        (2,2,2): -1


    }

    while True:
        match state:
            case 0:
                #checks if there are any codes in the queue before pulling from it
                if(len(codes_deque) == 0):
                    break

                region = codes_deque.popleft()
                region_code = RegionCodeGetter(region) + 1
                if codes_deque:
                    state = init_dict[codes_deque.popleft()[0]]
                else:
                    break

                print("On " + str(region_code) + " / 27 of the image, ")
            case 1:
                print("print the three digit codes.")
                state = -1
            case 2:
                print("print the code sentences.")
                state = -1
            case 3:
                print("print a snipet of the python code.")
                state = -1
            case 4:
                print("randomly sort the pixels.")
                state = -1
            case 5:
                print("sort the pixels.")
                state = -1
            case 6:
                print("print the hexadecimal data.")
                state = -1
            case 7:
                print("threshold the image.")
                if (len(codes_deque) == 0):
                    break
                
                thresh_code = codes_deque.pop()[0]

                thresh_type = cv2.THRESH_BINARY
                if (thresh_code[0] == 1):
                    thresh_type = cv2.THRESH_BINARY_INV
                if (thresh_code[0] == 2):
                    thresh_type = cv2.THRESH_TOZERO

                thresh_value = int((thresh_code[1] + thresh_code[2]) / 9 * 100) + 100
                merge_img = manip.ThreshApplier(img, region, thresh_type, thresh_value)
                state = -1
            case 8:
                print("create an image that is identical to the interpreter.")
                state = -1
            case 9:
                print("create a fractal pattern.")
                state = -1
            case 10:
                print("Print a statement.")
                state = -1
            case 11:
                print("Apply Canny Edge Detection.")
                merge_img = manip.CannyApplier(img, region)
                state = -1
            case -1:
                print("Skip Section.")
                state = 0

    return merge_img
            

#Converts the region code and turns it into a whole number of pixels 
def FractionToRegion(height, region_code):
    return int(height * round(region_code / 27, 2))

def RegionCodeGetter(region):
    return base3(region[0]) 

#converts a base3 series of digits into an integer
def base3(tuple):
    int_value = 0
    place = len(tuple) - 1

    for i in tuple:
        int_value += i * pow(3, (place))
        place -= 1
    return int_value 

