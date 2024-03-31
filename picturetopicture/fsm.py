from collections import deque
import cv2
import manip

'''
fsmRunner

The Finite State Machine that moves from state to state until the codes_deque is expended, working functions on the input image.

Parameters: 
codes_deque:    Deque, the deque of codes generated from codel analysis that functions as the function's input stream
img:            Img, the actual inupt image
img_name:       String, the file name of the imput image

Returns the output image
'''
def fsmRunner(codes_deque, img, img_name):
    region = 0
    state = 0
    prev_state = -1
    subimage_deque = deque()
    merge_img = img
    code_sentence = ""

    '''
    Legend:
    [Integer] [State]
    0          Start
    1          3 Digit Code
    2          Statement
    3          Python
    4          Random
    5          Sort
    6          JPEG
    7          Threshold
    8          Grayscale Threshold
    9          Fractal
    10         Print
    11         Canny
    -1         End

    '''
    #Assigns a state for the function code.
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
        (1,0,0): 5,
        (1,0,1): 5,
        (1,0,2): 5,
        (1,1,0): 6,
        (1,1,1): 7,
        (1,1,2): 9,
        (1,2,0): 4,
        (1,2,1): 4,
        (1,2,2): 4,
        (2,0,0): 4,
        (2,0,1): 4,
        (2,0,2): 4,
        (2,1,0): 4,
        (2,1,1): 4,
        (2,1,2): 8,
        (2,2,0): 8,
        (2,2,1): 8,
        (2,2,2): -1

    }

    #loops through the stream of base 3 codes until the stream is empty.
    while True:
        #chooses a Tower function based on the state of init_dict
        match state:
            #initial state.  Draws a region code and function code from the deque and goes to that function's state
            case 0:
                #checks if there are any codes in the queue before pulling from it
                if(len(codes_deque) == 0):
                    break

                #finds the region code for the statement.
                region = codes_deque.popleft()
                region_code = RegionCodeGetter(region) + 1
                #keeps running through the fsm as long as there are codes still in the deque.
                if codes_deque:
                    state_holder = codes_deque.popleft()
                    state = init_dict[state_holder[0]]
                else:
                    break
                
                #leaves the fsm if the deque doesn't have enough codes for the next statement
                if(len(codes_deque) == 0 and (base3(state_holder[0]) != 26 and (base3(state_holder[0])) != 14)):
                    break

                code_sentence += ("On " + str(region_code) + " / 27 of the image, ")
            #State for Base3
            case 1:
                print("Running Base3 function...")
                code_sentence += ("print the base 3 codes.\n")

                merge_img = manip.Base3Applier(img, region, state_holder, codes_deque.popleft(), codes_deque)

                state = 0
            #State for Sentence
            case 2:
                print("Running Sentence function...")

                code_sentence += ("print the code sentences.\n")
                merge_img = manip.SentenceApplier(img, region, code_sentence, state_holder, codes_deque.popleft())

                state = 0
            #State for Python
            case 3:
                print("Running Python function...")
                code_sentence += ("print a snipet of the Python code.\n")

                #chooses the file to pull text from based off of the last digit of the function code
                file = "manip.py"
                if(state_holder[0][2] == 0):
                    file = "picturetopicture.py"
                elif(state_holder[0][2] == 1):
                    file = "fsm.py"

                merge_img = manip.PythonApplier(img, region, state_holder, file)

                codes_deque.popleft()
                state = 0
            #State for Sort
            case 4:
                print("Running Sort function...")
                if (len(codes_deque) == 0):
                    break

                #chooses the value by which to sort pixels based off of the last two digits of the function code
                sort_code = base3(state_holder[0]) + 1
                sort_mode = "lightness"
                if(sort_code == 20):
                    sort_mode = "hue"
                elif(sort_code == 21 or sort_code == 22):
                    sort_mode = "saturation"
                elif(sort_code == 23 or sort_code == 24):
                    sort_mode = "intensity"
                elif(sort_code == 25 or sort_code == 26):
                    sort_mode = "minimum"


                properties = codes_deque.popleft()
                #determines the degree the pixels should be sorted at based on the first digit of the property code
                degree = 0
                if(properties[0][0] == 1):
                    degree = 45
                elif(properties[0][0] == 2):
                    degree = 90

    
                #determines percentage of color threshold to be sorted, out of 1.  Based on the third digit of the property code
                percent = .5
                if(properties[0][1] == 1):
                    percent = .75
                elif(properties[0][1] == 2):
                    percent = 1.0


                #determines the upper and lower bounds of the threshold, based on the second digit of the property code.  Pixels that fit within the bounds of the threshold get sorted.
                lower_bound = 0
                upper_bound = percent
                if(properties[0][2] == 1):
                    lower_bound = (1 - percent) / 2
                    upper_bound = (1 - percent) / 2 + percent
                elif(properties[0][2] == 2):
                    lower_bound = 1 - percent
                    upper_bound = 1


                code_sentence += ("sort the pixels by " + sort_mode + " within the bounds (" + str(lower_bound) + ", " + str(upper_bound) + "), sorting in direction " + str(degree) + " degrees.\n")

                merge_img = manip.SortApplier(img, region, sort_mode, lower_bound, upper_bound, degree)


                state = 0
            #State for Hexa
            case 5:
                print("Running Hexa function...")
                code_sentence += ("print the hexadecimal data.\n")
                merge_img = manip.HexaApplier(img, region, state_holder, codes_deque.popleft(), img_name)

                state = 0
            #State for Threshold (color)
            case 6:
                print("Running Threshold function...")
                code_sentence += ("threshold the image (color).\n")
                if (len(codes_deque) == 0):
                    break
                
                #chooses threshold type based on codel
                thresh_code = codes_deque.pop()[0]
                thresh_type = cv2.THRESH_BINARY
                if (thresh_code[0] == 1):
                    thresh_type = cv2.THRESH_BINARY_INV
                if (thresh_code[0] == 2):
                    thresh_type = cv2.THRESH_TOZERO

                #calculates value by which to threshold image
                thresh_value = int((thresh_code[1] + thresh_code[2]) / 9 * 100) + 100
                merge_img = manip.ThreshApplier(img, region, thresh_type, thresh_value, False)
                state = 0
            #State for Threshold (grayscale)
            case 7:
                print("Running Threshold function...")
                code_sentence += ("threshold the image (grayscale).\n")

                if (len(codes_deque) == 0):
                    break
                
                #chooses threshold type based on codel
                thresh_code = codes_deque.pop()[0]
                thresh_type = cv2.THRESH_BINARY
                if (thresh_code[0] == 1):
                    thresh_type = cv2.THRESH_BINARY_INV
                if (thresh_code[0] == 2):
                    thresh_type = cv2.THRESH_TOZERO

                #calculates value by which to threshold image
                thresh_value = int((thresh_code[1] + thresh_code[2]) / 9 * 100) + 100
                merge_img = manip.ThreshApplier(img, region, thresh_type, thresh_value, True)
                state = 0
            #State for Print
            case 8:
                print("Running Print function...")
                code_sentence += ("print a statement.\n")
                merge_img = manip.PrintApplier(img, region, state_holder, codes_deque.popleft(), codes_deque)

                #removes codes from the queue to match up with the iteration in manip.py
                while codes_deque:
                    if base3(codes_deque.popleft()[0]) == 0:
                        break

                state = 0
            #state for Canny
            case 9:
                print("Running Canny function...")
                code_sentence += ("apply Canny Edge Detection.\n")

                merge_img = manip.CannyApplier(img, region)
                state = 0
            #State for Skip
            case -1:
                print("Running Skip function...")
                code_sentence += ("skip section.\n")

                merge_img = manip.SkipApplier(img, region)
                state = 0
    print(code_sentence)
    return merge_img
            

'''
FractionToRegion

Converts the region code from a fraction of a total image into an absolute number of rows to affect 

Parameters:
height:         int, height of the image
region_code:    int, a fraction (out of 27) of the image to affect.  The statement's region code.

Returns: int, An absolute number of rows for the function to affect

'''
def FractionToRegion(height, region_code):
    return int(height * round(region_code / 27, 2))


'''
RegionCodeGetter

Parameters:
region: tuple, the region code in base 3 format

Returns: an integer representation of the base 3 tuple region code.

'''
def RegionCodeGetter(region):
    return base3(region[0]) 

'''
base3

converts a base3 three digit code into a base 10 integer

'''
def base3(tuple):
    int_value = 0
    place = len(tuple) - 1

    #converts each tuple digit one by one
    for i in tuple:
        int_value += i * pow(3, (place))
        place -= 1
    return int_value 

'''
codeToString

converts a base3 three digit code into a string

'''
def codeToString(code):
    return str(code[0]) + str(code[1]) + str(code[2])
