#from statemachine import StateMachine, State
from collections import deque

def fsmRunner(codes_deque):
    state = 0
    prev_state = -1

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

    while True:
        match state:
            case 0:
                region = base3(codes_deque.popleft())      
                if codes_deque:
                    state = init_dict[codes_deque.popleft()]
                else:
                    break

                print("On " + str(region) + " / 27 of the image, ")
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
                state = -1
            case 8:
                print("create an image that is identical to the interpreter.")
                state = -1
            case 9:
                print("create a fractal pattern.")
                state = -1
            case 10:
                print("Print a statement")
                state = -1
            case 11:
                print("Apply Canny Edge Detection.")
                state = -1
            case -1:
                print("")
                state = 0

            



#converts a base3 series of digits into an integer
def base3(tuple):
    int_value = 0
    place = len(tuple) - 1

    for i in tuple:
        int_value += i * pow(3, (place))
        place -= 1
    return int_value 


'''
#the finite state machine that runs through the code
class CodesStateMachine(codes_deque):
    #The States
    START_S = State(initial=True)
    Code_S = State()
    State_S = State()
    Python_S = State()
    Rand_S = State()
    Sort_S = State()
    JPEG_S = State()
    Thresh_S = State()
    Funct_S = State()
    Fractal_S = State()
    Print_S = State()
    Char_S = State()
    Canny_S = State()
    END_S = State(final=True)

    #Transitions
    #Transitions from Start_S to a Procedure State
    Code_Init = Start_S.to(Code_S)
    State_Init = Start_S.to(State_S)
    Python_Init = Start_S.to(Python_S)
    Rand_Init = Start_S.to(Rand_S)
    Sort_Init = Start_S.to(Sort_S)
    JPEG_Init = Start_S.to(JPEG_S)
    Thresh_Init = Start_S.to(Thresh_S)
    Funct_Init = Start_S.to(Funct_S)
    Fractal_Init = Start_S.to(Fractal_S)
    Print_Init = Start_S.to(Print_S)
    Canny_Init = Start_S.to(Canny_S)
    #Since nothing occurs at the Skip state, returns to START_S
    Skip_Init = Start_S.to.itself()

    #Transitions from a Procedure State to Start_S
    Code_Reset = Code_S.to(START_S)
    State_Reset = State_S.to(START_S)
    Python_Reset = Python_S.to(START_S)
    Rand_Reset = Rand_S.to(START_S)
    Sort_Reset = Sort_S.to(START_S)
    JPEG_Reset = JPEG_S.to(START_S)
    Thresh_Reset = Thresh_S.to(START_S)
    Funct_Reset = Funct_S.to(START_S)
    Fractal_Reset = Fractal_S.to(START_S)
    Print_Reset = Prnt_S.to(START_S)
    Char_Reset = Char_S.to(START_S)
    Canny_Reset = Canny_S.to(START_S)

    #Transitions to Char_S (for building a string)
    Char_Init = Print_S.to(Char_S)
    Char_Cycle = Char_S.to.itself()

    #Transitions to END_S
    End_Init = START_S.to(END_S)
    End_Code = Code_S.to(END_S)
    End_Python = Python_S.to(END_S)
    End_Rand = Rand_S.to(END_S)
    End_Sort = Sort_S.to(END_S)
    End_JPEG = JPEG_S.to(END_S)
    End_Thresh = Thresh_S.to(END_S)
    End_Funct = Funct_S.to(END_S)
    End_Fractal = Fractal_S.to(END_S)
    End_Print = Print_S.to(END_S)
    End_Char =  Char_S.to(END_S)
    End_Canny = Canny_S.to(END_S)




    def __init__(self):
        self.statement = ""
'''