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
    message += "@" + str(segment) + "\n"
    message += "A=M+D\n"
    message += "D=M\n"
    pushValue()

#accepted parameter for segement: @LCL, @ARG, @THIS, @THAT, 
def popSegment(segment, value):
    global message
    #need to find the address to pop into (MAKE SURE TO STORE IN TEMP REGISTER)
    message += "@" + str(value) + "\n" 
    message += "D=A\n"             # D = value 
    message += "@" + str(segment) + "\n"
    message += "A=M\n"             #A points to the base address of the segment. 
    message += "D=D+A\n"           # now let d be the target address of LCL+value
    message += "@R13\n"
    message += "M=D\n" 

    #pop the top value off the stack
    decrementSP()       # SP is getting ready to pop the top value off the stack 
    message += "A=M\n"             #A points to the actual memory location of the top value
    message += "D=M\n"             # D = get top of the stack value 

    message += "@R13\n"
    message += "A=M\n"
    message += "M=D\n"
    
#--------------------------temp push and pop--------------------------#

#temp segment is fixed at 5-12, so we can just add the value to 5 to get the correct address.
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

#pointer segment is fixed at 3-4, so we can just add the value to 3 to get the correct address.
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

#acceptable parameters: +, -, &, | 
def arithmetic(command):
    global message

    decrementSP() 
    message += "D=M\n" # y

    decrementSP() 
    message += "A=M\n" 
    message += "D=D" + command + "M\n" # x (command) y

    pushValue() 


#--------------------------static pop and push--------------------------#

# The name of the variable is file.value, where file is the name of the current file.
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


#--------------------------reading in the files--------------------------#

def readFile(fileName):
    global message
    message = ""
    global file
    file = fileName.split("/")[-1].split(".")[0]
    with open(fileName) as f:
        lines = f.readlines()
    for line in lines: 
        # remove comments and whitespace
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
                else:
                    message += "Incorrect command: " + parts[0]    
                arithmetic(parts[0])

            elif parts[0] in ["eq", "gt", "lt"]:
                logical(parts[0])

            else:
                message += "Incorrect command: " + parts[0]
    
    return lines

def writeFile(outputFile, message):
    with open(outputFile, "w") as f:
        f.write(message)


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
