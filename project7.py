
def pushConstant(value):
    message  = "@" + str(value) + "\n"
    message += "D=A\n"
    message += pushValue()
    return message

#apprently I dont need to pop constant?????
def popConstant():
    message = decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    return message

#accepted parameter for segement: @LCL, @ARG, @THIS, @THAT, 
def pushSegment(segment, value):
    message  = "@" + str(value) + "\n"
    message += "D=A\n"
    message += "@" + str(segment) + "\n"
    message += "A=M+D\n"
    message += "D=M\n"
    message += pushValue()
    return message

#accepted parameter for segement: @LCL, @ARG, @THIS, @THAT, 
def popSegment(segment, value):
    #need to find the address to pop into (MAKE SURE TO STORE IN TEMP REGISTER)
    message = "@" + str(value) + "\n" 
    message += "D=A\n"             # D = value 
    message += "@" + str(segment) + "\n"
    message += "A=M\n"             #A points to the base address of the segment. 
    message += "D=D+A\n"           # now let d be the target address of LCL+value
    message += "@R13\n"
    message += "M=D\n" 

    #pop the top value off the stack
    message = decrementSP()       # SP-- 
    message += "A=M\n"             #A points to the actual memory location of the top value
    message += "D=M\n"             # D = get top of the stack value 

    message += "@R13\n"
    message += "A=M\n"
    message += "M=D\n"
    
    return message

#--------------------------HELPER FUNCTIONS--------------------------#
def pushValue():
    message = "@SP\n"
    message += "A=M\n"
    message += "M=D\n"
    message += incrementSP()
    return message

def decrementSP():
    message = "@SP\n"
    message += "M=M-1\n"
    return message

def incrementSP():
    message = "@SP\n"
    message += "M=M+1\n"
    return message