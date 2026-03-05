import os
import sys

global message

#-----------------------------------------------------------project 8---------------------------------------------------------------------------------------------#


def bootstrap():
    global message, currentFunction
    message += "@256\n"
    message += "D=A\n"
    message += "@SP\n"
    message += "M=D\n"

    oldFunction = currentFunction
    currentFunction = ""
    writeCall("Sys.init", 0)
    currentFunction = oldFunction

def getLabel(labelName):
    global currentFunction
    if currentFunction != "":
        return currentFunction + "$" + labelName
    return labelName

def writeLabel(labelName):

    global message, currentFunction
    
    message += "(" + getLabel(labelName) + ")\n"

def writeGoto(labelName):

    global message, currentFunction
    
    message += "@" + getLabel(labelName) + "\n"
    message += "0;JMP\n"

def writeIfGoto(labelName):

    global message, currentFunction

    decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    message += "@" + getLabel(labelName) + "\n"
    message += "D;JNE\n"


def writeFunction(fName, localNums):
    global message, currentFunction

    currentFunction = fName
    message += "(" + fName + ")\n"

    for i in range(localNums):
        pushConstant(0)

def writeCall(fName, argsNums):
    global message, currentFunction, count

    returnAddress = fName + "$ret." + str(count)
    count += 1

    #push return address
    message += "@" + returnAddress + "\n"
    message += "D=A\n"
    pushValue()

    pushSegmentBase("LCL")
    pushSegmentBase("ARG")
    pushSegmentBase("THIS")
    pushSegmentBase("THAT")

    #ARG = SP - numArgs - 5
    message += "@SP\n"
    message += "D=M\n"
    message += "@" + str(argsNums + 5) + "\n"
    message += "D=D-A\n"
    message += "@ARG\n"
    message += "M=D\n"

    #LCL = SP
    message += "@SP\n"
    message += "D=M\n"
    message += "@LCL\n"
    message += "M=D\n"

    message += "@" + fName + "\n"
    message += "0;JMP\n"

    #declare return address label
    message += "(" + returnAddress + ")\n"

def writeReturn():
    global message, currentFunction

    #FRAME = LCL
    message += "@LCL\n"
    message += "D=M\n"
    message += "@R13\n"
    message += "M=D\n"

    # RET = *(FRAME - 5)
    message += "@R13\n"
    message += "D=M\n"
    message += "@5\n"
    message += "A=D-A\n"
    message += "D=M\n"
    message += "@R14\n"
    message += "M=D\n"

    
    #*ARG = pop()
    decrementSP()

    message += "A=M\n"
    message += "D=M\n"
    message += "@ARG\n"
    message += "A=M\n"
    message += "M=D\n"

    #sp = ARG + 1
    message += "@ARG\n"
    message += "D=M\n"
    message += "D=D+1\n"
    message += "@SP\n"
    message += "M=D\n"

    #THAT = *(FRAME - 1)
    frameDecrment("THAT", 1)

    #THIS = *(FRAME - 2)
    frameDecrment("THIS", 2)

    #ARG = *(FRAME - 3)
    frameDecrment("ARG", 3)

    #LCL = *(FRAME - 4)
    frameDecrment("LCL", 4)

    #goto RET
    message += "@R14\n"
    message += "A=M\n"
    message += "0;JMP\n"

def frameDecrment(segment, offset):
    global message
    message += "@R13\n"
    message += "D=M\n"
    message += "@" + str(offset) + "\n"
    message += "A=D-A\n"
    message += "D=M\n"
    message += "@" + segment + "\n"
    message += "M=D\n"

def pushSegmentBase(segment):
    global message
    message += "@" + segment + "\n"
    message += "D=M\n"
    pushValue()

#-----------------------------------------------------------project 7---------------------------------------------------------------------------------------------#

#--------------------------constant push and pop--------------------------#

def pushConstant(value):
    global message
    message  += "@" + str(value) + "\n" # D = value
    message += "D=A\n"
    pushValue()

#--------------------------SEGMENT POP AND PUSH--------------------------#
#accepted parameter for segement: @LCL, @ARG, @THIS, @THAT, 
def pushSegment(segment, value):
    global message
    message  += "@" + str(value) + "\n"
    message += "D=A\n"
    message += str(segment) + "\n"
    message += "A=D+M\n"
    message += "D=M\n"
    pushValue()

def popSegment(segment, value):
    global message
    message += "@" + str(value) + "\n" 
    message += "D=A\n"             # D = value 
    message += str(segment) + "\n"  
    message += "D=D+M\n"   
    message += "@R13\n"
    message += "M=D\n" 

    decrementSP()       # SP is getting ready to pop the top value off the stack 
    message += "A=M\n"             #A points to the actual memory location of the top value
    message += "D=M\n"             # D = get top of the stack value 

    message += "@R13\n"
    message += "A=M\n"
    message += "M=D\n"
    
#--------------------------temp push and pop--------------------------#
def pushTemp(value):
    global message
    message  += "@" + str(5 + value) + "\n"
    message += "D=M\n"
    pushValue()

def popTemp(value):
    global message
    decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    message += "@" + str(5 + value) + "\n"
    message += "M=D\n"

#--------------------------pointer push and pop--------------------------#
def pushPointer(value):
    global message
    message  += "@" + str(3 + value) + "\n"
    message += "D=M\n"
    pushValue()

def popPointer(value):
    global message
    decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    message += "@" + str(3 + value) + "\n"
    message += "M=D\n"

#--------------------------Arithmetic commands--------------------------#
def arithmetic(command):
    global message
    # SP--
    message += "@SP\n"
    message += "AM=M-1\n"
    message += "D=M\n"        # D = y

    # SP--
    message += "@SP\n"
    message += "AM=M-1\n"     # A now points to x

    if command == "+":
        message += "M=D+M\n"
    elif command == "-":
        message += "M=M-D\n"
    elif command == "&":
        message += "M=M&D\n"
    elif command == "|":
        message += "M=M|D\n"

    incrementSP()       # SP++

#--------------------------static pop and push--------------------------#
def pushStatic(value):
    global message
    message  += "@" + file + "." + str(value) + "\n"
    message += "D=M\n"
    pushValue()

def popStatic(value):
    global message
    decrementSP()
    message += "A=M\n"
    message += "D=M\n"
    message += "@" + file + "." + str(value) + "\n"
    message += "M=D\n"

#--------------------------logical commands--------------------------#
def logical(command):
    global message, count
    count += 1 # need to make sure that the labels are unique for each logical command
    true = f"EQ_{count}"
    false = f"EQ_f{count}"

    decrementSP()
    message += "A=M\n"
    message += "D=M\n"   # Store the top value in D (y)

    decrementSP()
    message += "A=M\n"
    message += "D=M-D\n" # Compute x - y and store result in D

    # Conditional jump based on the comparison
    message += "@" + true + "\n"
    if command == "eq":
        message += "D;JEQ\n"
    elif command == "gt":
        message += "D;JGT\n"
    elif command == "lt":
        message += "D;JLT\n"
    
    #set D = 0 if condition is not met
    message += "D=0\n"
    message += "@" + false + "\n"
    message += "0;JMP\n"
    message += "(" + true + ")\n"

    #set D = -1 if condition is met
    message += "D=-1\n"
    message += "(" + false + ")\n"

    pushValue()

#--------------------------HELPER FUNCTIONS--------------------------#
def pushValue():
    global message
    message += "@SP\n"
    message += "A=M\n"
    message += "M=D\n"
    incrementSP()

def decrementSP():
    global message
    message += "@SP\n"
    message += "M=M-1\n"

def incrementSP():
    global message
    message += "@SP\n"
    message += "M=M+1\n"

#--------------------------reading in the files--------------------------#
def readFile(fileName):
    global message
    global file

    fileName = os.path.abspath(fileName)


    if os.path.isdir(fileName):
        for i in os.listdir(fileName):
            if i.endswith(".vm"):
                readFile(os.path.join(fileName, i))
        return  
    
    if not fileName.endswith(".vm"):
        return
    
    file = os.path.basename(fileName).split(".")[0]

    with open(fileName) as f:
        lines = f.readlines()

    for line in lines:
        line = line.split("//")[0].strip()
        if line == "":
            continue

        parts = line.split()

        if parts[0] == "push":
            segment = parts[1]
            value = int(parts[2])
            if segment == "constant":
                pushConstant(value)
            elif segment == "local":
                pushSegment("@LCL", value)
            elif segment == "argument":
                pushSegment("@ARG", value)
            elif segment == "this":
                pushSegment("@THIS", value)
            elif segment == "that":
                pushSegment("@THAT", value)
            elif segment == "temp":
                pushTemp(value)
            elif segment == "pointer":
                pushPointer(value)
            elif segment == "static":
                pushStatic(value)

        elif parts[0] == "pop":
            segment = parts[1]
            value = int(parts[2])
            if segment == "local":
                popSegment("@LCL", value)
            elif segment == "argument":
                popSegment("@ARG", value)
            elif segment == "this":
                popSegment("@THIS", value)
            elif segment == "that":
                popSegment("@THAT", value)
            elif segment == "temp":
                popTemp(value)
            elif segment == "pointer":
                popPointer(value)
            elif segment == "static":
                popStatic(value)

        elif parts[0] in ["add", "sub", "and", "or"]:
            ops = {"add": "+", "sub": "-", "and": "&", "or": "|"}
            arithmetic(ops[parts[0]])

        elif parts[0] in ["neg", "not"]:
            message += "@SP\n"
            message += "A=M-1\n"   # point to top of stack
            if parts[0] == "neg":
                message += "M=-M\n"
            elif parts[0] == "not":
                message += "M=!M\n"

        elif parts[0] in ["eq", "gt", "lt"]:
            logical(parts[0])

        elif parts[0] == "label":
            writeLabel(parts[1])

        elif parts[0] == "goto":
            writeGoto(parts[1])

        elif parts[0] == "if-goto":
            writeIfGoto(parts[1])
        elif parts[0] == "function":
            writeFunction(parts[1], int(parts[2]))
        elif parts[0] == "call":
            writeCall(parts[1], int(parts[2]))
        elif parts[0] == "return":
            writeReturn()


def writeToFile():
    global message

    #code credit to stack overflow for this part: https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    folder = os.path.dirname(path)
    base_name = os.path.basename(path).split(".")[0]
    output_path = os.path.join(folder, base_name + ".asm")    

    with open(output_path, "w") as outfile:
        outfile.write(message)



#--------------------------RUN THE CODE--------------------------#


#ask the user for the path to the file or directory they want to translate, then read in the file and write to the output file

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = input("Enter the path to the file or directory to translate: ")

count = 0
message = ""
file = ""
currentFunction = ""

#bootstrap is not required for BasicLoop, SimpleFunction
#bootstrap is required for FibonacciElement, Nested Call, and StaticTest because they all call Sys.init
bootstrap()

readFile(path)
print(message)
writeToFile()
print("Output written to "+ os.path.splitext(path)[0] + ".asm")