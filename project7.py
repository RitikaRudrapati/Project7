
def pushConstant(value):
    message  = "@" + str(value) + "\n"
    message += "D=A\n"
    message += pushValue()
    return message

def popConstant():
    message = decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    return message

def pushLocal(value):
    message  = "@" + str(value) + "\n"
    message += "D=A\n"
    message += "@LCL\n"
    message += "A=M+D\n"
    message += "D=M\n"
    message += pushValue()
    return message

def popLocal(value):
    message  = decrementSP() #points sp to the top value 
    message += "A=M\n" #D = RAM[SP]
    message += "D=M\n" #D has the value we want to store in local[i]

    message += "@LCL\n"

    
    return message

#--------------------------HELPER FUNCTIONS--------------------------#
def pushValue():
    message += "@SP\n"
    message += "A=M\n"
    message += "M=D\n"
    message += "@SP\n" 
    message += "M=M+1\n"
    return message

def decrementSP():
    message  = "@SP\n"
    message += "M=M-1\n"
    return message