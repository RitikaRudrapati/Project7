
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
    #need to find the address to pop into (MAKE SURE TO STORE IN TEMP REGISTER)
    message += "@" + str(value) + "\n" 
    message += "D=A\n"             # D = value 
    message += "@LCL\n"
    message += "A=M\n"             #A points to the base address of the LCL segment. 
    message += "D=D+A\n"           # now let d be the target address of LCL+value
    message += "@R13\n"
    message += "M=D\n" 

    #pop the top value off the stack
    message  = decrementSP()       # SP-- 
    message += "A=M\n"             #A points to the actual memory location of the top value
    message += "D=M\n"             # D = get top of the stack value 

    message += "@R13\n"
    message += "A=M"
    message += "M=D"

    

    message += incrementSP()       # increment SP back

    

    return message

#--------------------------HELPER FUNCTIONS--------------------------#
def pushValue():
    message += "@SP\n"
    message += "A=M\n"
    message += "M=D\n"
    message += incrementSP()
    return message

def decrementSP():
    message  = "@SP\n"
    message += "M=M-1\n"
    return message

def incrementSP():
    message  = "@SP\n"
    message += "M=M+1\n"
    return message