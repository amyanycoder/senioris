from statemachine import StateMachine, State

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

    

