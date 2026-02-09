import os

global message

#--------------------------constant push and pop--------------------------#
count = 0

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
    message += "A=M+D\n"
    message += "D=M\n"
    pushValue()

def popSegment(segment, value):
    global message
    message += "@" + str(value) + "\n" 
    message += "D=A\n"             # D = value 
    message += str(segment) + "\n"
    message += "A=M\n"             #A points to the base address of the segment. 
    message += "D=D+A\n"           # now let d be the target address of LCL+value
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
    decrementSP() 
    message += "D=M\n" # y
    decrementSP() 
    message += "A=M\n" 
    message += "D=D" + command + "M\n" # x (command) y
    pushValue() 

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
    message = ""
    global file
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
            if parts[0] == "add":
                parts[0] = "+"
            elif parts[0] == "sub":
                parts[0] = "-"
            elif parts[0] == "and":
                parts[0] = "&"
            elif parts[0] == "or":
                parts[0] = "|"
            arithmetic(parts[0])
        elif parts[0] in ["eq", "gt", "lt"]:
            logical(parts[0])
        else:
            message += "Incorrect command: " + parts[0]

def writeToFile():
    global message

    #code credit to stack overflow for this part: https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    folder = os.path.dirname(test_path)
    base_name = os.path.basename(test_path).split(".")[0]
    output_path = os.path.join(folder, base_name + ".asm")    

    with open(output_path, "w") as outfile:
        outfile.write(message)



#--------------------------RUN THE CODE--------------------------#

#hardcode this for testing purposes, can change it to read in a directory of files later 
test_path = r"C:\Users\ritik\ECS_2\project7\test.vm"

readFile(test_path)
writeToFile()