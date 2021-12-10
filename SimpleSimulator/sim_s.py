from sys import stdin
import matplotlib.pyplot as plt


# Opcodes using Ifs.
# labels ->    .{label_name}
# etc...
# IMM -> "#"
# PP-> labels list
# wieght-> loop:
# q
# e
# bne loop
# total mem/2 bytes - no. of units->> ceil(log(n)) no. of bytes to address memory locations-> 8 bits
# memory-(2^9 B) ||  2^4 B bit addressable->(5 bits)
# loop : (0x00 16s(0x03))
# from inspect import stack
# *val is an address whose value needs to be stored
# a = []
# b = []
# # i = 1
# file = open('a.txt', 'r')
# for instruction in file.readlines():
#     instruct_body = instruction.split()
#     if instruct_body[0][0:2:] == "//":
#         continue
#     if instruct_body[0].upper() == "LD":
#         b.append([i, "LOAD"])
#         a.append([i, "0x00"])
#         reg = hex(int(instruct_body[1]))
#         b.append([i, "R "+instruct_body[1]])
#         a.append([i, reg])
#         if instruct_body[2][0] == "$":
#             b.append([i, "IMM", instruct_body[2][1::]])
#             val = hex(int(instruct_body[2][1::]))
#             a.append([i, val])
#         else:
#             b.append([i, "R " + instruct_body[2]])
#             val = '* ' + str(hex(int(instruct_body[2])))
#             a.append([i, val])
#     i+=1
# print(a)
# print(b)


operations = {'00000': 'A', '00001': 'A', '00010': 'B', '00011': 'C', '00100': 'D', '00101': 'D', '00110': 'A', '00111': 'C',
              '01000': 'B', '01001': 'B', '01010': 'A', '01011': 'A', '01100': 'A', '01101': 'C', '01110': 'C',
              '01111': 'E', '10000': 'E', '10001': 'E', '10010': 'E', '10011': 'F'}


# class Registers:
#     count = 0
#     def __init__(self):
#         Registers.count+=1
#         self.id= Registers.count
#         self.str = "0"*16
#         self.val = 0

# R1 = Registers()
# R2 = Registers()
# R3 = Registers()
# R4 = Registers()
# R5 = Registers()
# R6 = Registers()
# R7 = Registers()
# class fRegister:
#     def __init__(self):
#         self.V = 0
#         self.G = 0
#         self.L = 0
#         self.E = 0
#
# fR = fRegister()


def Rfiller(a):
    b = str(bin(a))[2::]
    b = "0"*(3-len(b))+b
    return b


def MIfiller(a):
    b = str(bin(a))[2::]
    b = "0"*(8-len(b))+b
    return b


def BFiller(a):  # changed
    b = str(bin(a))[2::]
    b = "0"*(16-len(b))+b
    # b = "0"*(16-len(b[-8:]))+b[-8:] #use for overflow handling
    return b


def AddressFiller(a):
    b = str(bin(a))[2::]
    b = "0" * (8 - len(b)) + b
    return b


# flagRegister = [0]*16 #changed
global V, L, G, E
V = "0"
G = "0"
L = "0"
E = "0"


def add(a, b, c):  # changed
    global V
    V = "0"
    if((registers[b] + registers[c]) > 65535 or (registers[b] + registers[c]) < 0):
        V = "1"
    registers[a] = registers[b] + registers[c]
    if V == "1":
        c = registers[a]//65536
        registers[a] -= (65536*c)
    registers_display[a] = BFiller(registers[a])


def sub(a, b, c):  # changed
    global V
    V = "0"
    if(registers[b] < registers[c]):
        V = "1"
        registers[a] = 0
        registers_display[a] = BFiller(registers[a])
    else:
        registers[a] = registers[b] - registers[c]
        registers_display[a] = BFiller(registers[a])


def mov_im(a, b):
    registers[a] = b
    registers_display[a] = BFiller(registers[a])


def mov(a, b):
    registers[a] = registers[b]
    registers_display[a] = registers_display[b]


""" def mov_f(a, b):  # changed
    registers[a] = b
    registers_display[a] = BFiller(registers[a]) """


def mov_f(a):  # changed
    global V, L, G, E
    registers[a] = int(V + L + G + E, 2)
    registers_display[a] = BFiller(registers[a])


def ld(a, b):
    registers[a] = memory[b]
    registers_display[a] = memory_dis[b]


def st(a, b):
    memory[b] = registers[a]
    memory_dis[b] = registers_display[a]


def mul(a, b, c):  # changed
    global V
    V = "0"
    if((registers[b] * registers[c]) > 65535 or (registers[b] * registers[c]) < 0):
        V = "1"
    registers[a] = registers[b] * registers[c]
    if V == "1":
        c = registers[a]//65536
        registers[a] -= (65536*c)
    registers_display[a] = BFiller(registers[a])


def div(b, c):
    if(registers[c]==0):
        print("ERROR @Cycle "+str(cycle)+": Divison by zero error")
        quit()
    registers[0] = registers[b]//registers[c]
    registers_display[0] = BFiller(registers[0])
    registers[1] = registers[b] % registers[c]
    registers_display[1] = BFiller(registers[1])


def rs(a, imm):
    if imm >= 16:
        registers_display[a] = "0"*16
        registers[a] = 0
    else:
        registers_display[a] = "0"*imm + registers_display[a][:-imm:]
        registers[a] = int(registers_display[a], 2)


def ls(a, imm):
    if imm >= 16:
        registers_display[a] = "0" * 16
        registers[a] = 0
    else:
        registers_display[a] = registers_display[a][imm:] + "0" * imm
        registers[a] = int(registers_display[a], 2)


def eor(a, b, c):
    registers_display[a] = ""
    for i in range(16):
        if registers_display[b][i] == registers_display[c][i]:
            registers_display[a] += "0"
        else :
            registers_display[a] += "1"
    registers[a] = int(registers_display[a], 2)


def orr(a, b, c):
    registers[a] = registers[c] | registers[b]
    registers_display[a] = BFiller(registers[a])


def annd(a, b, c):
    registers[a] = registers[c] & registers[b]
    registers_display[a] = BFiller(registers[a])


def nott(a, b):
    registers_display[a] = ""
    for i in registers_display[b]:
        if i == "1":
            registers_display[a] += "0"
        elif i == "0":
            registers_display[a] += "1"



def cmp(a, b):
    global V, L, G, E
    G = "0"
    L = "0"
    E = "0"
    if registers[a] > registers[b]:
        G = "1"
    if registers[a] == registers[b]:
        E = "1"
    if registers[a] < registers[b]:
        L = "1"


""" def jmp(a):
    # hlt()
    # code.seek(int(a, 2), 0)
    fun_for_sim(a)
    return """


def jmp(a):
    return a


""" def jlt(a):
    global L
    if (L == "1"):
        jmp(a)
    return
def jgt(a):
    global G
    if (G == "1"):
        jmp(a)
    return
def je(a):
    global E
    if (E == "1"):
        jmp(a)
    return """


def jlt(a, pc):
    global L
    if (L == "1"):
        return a
    return pc + 1


def jgt(a, pc):
    global G
    if (G == "1"):
        return a
    return pc + 1


def je(a, pc):
    global E
    if (E == "1"):
        return a
    return pc + 1


def hlt():
    quit()


def resetFlags():
    global V, L, G, E
    V = "0"
    G = "0"
    L = "0"
    E = "0"


type = {'A': (2, 3, 3, 3, 0), 'B': (0, 3, 0, 0, 8), 'C': (5, 3, 3, 0, 0), 'D': (
    0, 3, 0, 0, 8), 'E': (3, 0, 0, 0, 8), 'F': (11, 0, 0, 0, 0)}
# 0th-> unused,reg1, reg2, reg3, mem/imm.
code = ''
for line in stdin:
    if line == '':
        break
    code += line


memory = [0]*256
memory_dis = ["0000000000000000"]*256
registers = [0]*7
registers_display = ["0"*16]*7
mac_code = ""
check = 0
labels = {}
labelsI = []
i = 0
vars = {}
j = -1
for i in code.splitlines():
    j += 1
    memory_dis[j] = i
    memory[j] = int(memory_dis[j], 2)
# code for var....-> using preprocessor loop(till instruct_root  == var....append lines of code to a str s...

global instruct_root_p
vcount = 0
vflag = 0
global Ninstr
# for preprocessor in code.readlines():  #changed
#     if preprocessor == "\n":
#         continue
#     instruct_root_p = preprocessor.split()
#     if instruct_root_p[0].lower() == "var":
#         if vflag==1:
#             print("ERROR: Declare variables only at the top")
#             quit()
#         if len(instruct_root_p)!=2:
#             print("ERROR: Incorrect number of operands provided.")
#             quit()
#         if instruct_root_p[1] in ["FLAGS","R0","R1","R2","R3","R4","R5","R6"] or instruct_root_p[1].lower() in operations.keys():
#             print("ERROR: Illegal use of reserved key words(register name, operation name).")
#             quit()
#             #raise Exception("Illegal use of reserved key words(register name, operation name).")
#         if instruct_root_p[1] in labels.keys():
#             print("ERROR: Label with given variable name already exists.")
#             quit()
#             #raise Exception("Label with given variable name already exists.")
#         if instruct_root_p[1] not in vars:
#             vars[instruct_root_p[1]] = vcount
#             vcount+=1
#             continue
#     vflag=1
#     i+=1
#     if instruct_root_p[0][-1] == ":":
#         if instruct_root_p[0][:-1:] in ["FLAGS","R0","R1","R2","R3","R4","R5","R6"] or instruct_root_p[0][:-1:].lower() in operations.keys():
#             print("ERROR: Illegal use of reserved key words(register name, operation name).")
#             quit()
#             #raise Exception("Illegal use of reserved key words(register name, operation name).")
#         if instruct_root_p[0][:-1:] in vars.keys():
#             print("ERROR: Variable with given label name already exists.")
#             quit()
#             #raise Exception("Variable with given label name already exists.")
#         if instruct_root_p[0][:-1:] in labels:
#             continue
#         else:
#             labels[instruct_root_p[0][:-1:]] = AddressFiller(i-1)
#
#     Ninstr = i
#
# #if instruct_root_p[0] != "hlt": #changed
# if instruct_root_p[-1] != "hlt":
#     print("ERROR: No exit statement in code.")
#     quit()
#     #raise Exception("No exit statement in code.")

# for i in vars.keys():
#     vars[i] = AddressFiller(Ninstr + vars[i])
#

# code.seek(0, 0)#change if file input not req. #changed

""" pc = -1

def fun_for_sim(index_of_branch):
    global check, memory, memory_dis, registers, registers_display, V, L, G, E
    for instruction_root_index in range(index_of_branch, len(memory)):  #changed
        print(MIfiller(instruction_root_index), end=" ")
        for reg in registers_display:
            print(reg, end= " ")
        print(('0'*12)+V+L+G+E)
        instruction_root = memory_dis[instruction_root_index]
        # if instruction_root == "\n":
        #     continue
        opcode = instruction_root[:5:]
        interpreted = operations.get(opcode)
        global pc
        pc+=1
        # instruct_root = instruction.split()

        # if instruct_root[0][0:2] == "//" or instruct_root[0].lower() == "var":
        #     continue
        # if instruct_root[0][-1] == ":":
        #     instruct_root.pop(0)
        # if instruct_root[0].lower() not in operations or instruct_root[0].lower()=="mov_im" or instruct_root[0].lower()=="mov_f":
        #     print('ERROR: '+instruct_root[0] + " is not a valid command")
        #     quit()
            #raise Exception(instruct_root[0] + " is not a valid command")
        # if instruct_root[0].lower() == "mov" and instruct_root[2][0] == "$":
        #     instruct_root[0] = "mov_im"
        # if instruct_root[0].lower() == "mov" and instruct_root[2] == "FLAGS":
        #     instruct_root[0] = "mov_f"

        # if(instruct_root[0].lower() not in operations.keys()):
        #     print("ERROR: Illegal operation name used ")
        #     quit()
            #raise Exception("Illegal operation name used ")
        # interpreted = operations.get(instruct_root[0].lower())

        # mac_code += interpreted[0]
        # mac_code += "0" * type.get(interpreted[1])[0]
        # if interpreted[:5:] != 'C' and instruct_root[0] != "mov_f" and "FLAGS" in instruct_root:
        #     print("ERROR: Illegal use of FLAGS register")
        #     quit()
            #raise Exception("Illegal use of FLAGS register")
        #
        # if interpreted[1] == 'A':
        #     if len(instruct_root)!=4:
        #         print("ERROR: Incorrect number of operands provided.")
        #         quit()
        #     r_names=["R0","R1","R2","R3","R4","R5","R6"]
        #     if (instruct_root[1] not in r_names or instruct_root[2] not in r_names or instruct_root[3] not in r_names):
        #         print("ERROR: Illegal register name used")
        #         quit()
        #         #raise Exception("Illegal register name used")
        #     mac_code+=Rfiller(int(instruct_root[1][1::]))
        #     mac_code+=Rfiller(int(instruct_root[2][1::]))
        #     mac_code+=Rfiller(int(instruct_root[3][1::]))

        if interpreted == "A":
            a = int(instruction_root[7:10:], 2)
            b = int(instruction_root[10:13:], 2)
            c = int(instruction_root[13::], 2)
            if opcode == '00000':
                add(a, b, c)

            if opcode == '00001':
                sub(a, b, c)

            if opcode == '00110':
                mul(a, b, c)

            if opcode == '01010':
                eor(a, b, c)

            if opcode == '01011':
                orr(a, b, c)

            if opcode == '01100':
                annd(a, b, c)



        elif interpreted == 'B' : #changed
            # if len(instruct_root)!=3:
            #     print("ERROR: Incorrect number of operands provided.")
            #     quit()
            # r_names=["R0","R1","R2","R3","R4","R5","R6"]
            # if (instruct_root[1] not in r_names):
            #     print("ERROR: Illegal register name used")
            #     quit()
            #     #raise Exception("Illegal register names used")
            # if (int(instruct_root[2][1::])>255 or int(instruct_root[2][1::])<0):
            #     print("ERROR: Illegal Immediate values")
            #     quit()
            #     #raise Exception("Illegal Immediate values")
            #
            # mac_code+=Rfiller(int(instruct_root[1][1::]))
            # mac_code+=MIfiller(int(instruct_root[2][1::]))
            a = int(instruction_root[5:8:], 2)
            b = int(instruction_root[8::], 2)
            if opcode == "00010":
                mov_im(a, b)

            if opcode == "01000":
                rs(a, b)

            if opcode == "01001":
                ls(a, b)

        # elif instruct_root[0] == "mov_f" and interpreted[1] == 'C': #changed
        #         if len(instruct_root)!=3:
        #             print("ERROR: Incorrect number of operands provided.")
        #             quit()
        #         r_names=["R0","R1","R2","R3","R4","R5","R6"]
        #         if (instruct_root[1] not in r_names):
        #             print("ERROR: Illegal register name used")
        #             quit()
        #             #raise Exception("Illegal register names used")
        #         mac_code+=Rfiller(int(instruct_root[1][1::]))
        #         #mac_code+=MIfiller(int((8*int(V))+(4*int(L))+(2*int(G))+int(E))) #or we can make it like a regular mov with 2 regs by putting in address of FLAGS reg as 111
        #         mac_code+='111'
        #         mov_f(int(instruct_root[1][1::]), int('0'*12+V+L+G+E,2))#((8*int(V))+(4*int(L))+(2*int(G))+int(E))


        # elif interpreted[1] == 'C' and instruct_root[0] != "mov_f":
            # if len(instruct_root)!=3:
            #     print("ERROR: Incorrect number of operands provided.")
            #     quit()
            # r_names=["R0","R1","R2","R3","R4","R5","R6"]
            # if (instruct_root[1] not in r_names or instruct_root[2] not in r_names):
            #     print("ERROR: Illegal register name used")
            #     quit()
            #     #raise Exception("Illegal register name used")
            # mac_code+=Rfiller(int(instruct_root[1][1::]))
            # mac_code+=Rfiller(int(instruct_root[2][1::]))
        if interpreted == 'C':
            a = int(instruction_root[10:13:], 2)
            b = int(instruction_root[13::], 2)
            if opcode == '00011':
                mov(a, b)

            if opcode == '00111':
                div(a, b)

            if opcode == '01101':
                nott(a, b)

            if opcode == '01110':
                cmp(a, b)

        elif interpreted == 'D':
            # if len(instruct_root)!=3:
            #     print("ERROR: Incorrect number of operands provided.")
            #     quit()
            # r_names=["R0","R1","R2","R3","R4","R5","R6"]
            # if (instruct_root[1] not in r_names):
            #     print("ERROR: Illegal register name used")
            #     quit()
                #raise Exception("Illegal register name used")
            # if instruct_root[2] not in vars:
            #     print("Definition Error:  Variable '" + instruct_root[2] + "' not Defined")
            #     quit()
            #     #raise Exception("Definition Error:  Variable '" + instruct_root[2] + "' not Defined")
            #
            # mac_code += Rfiller(int(instruct_root[1][1::]))
            # mac_code += vars[instruct_root[2]]
            a = int(instruction_root[5:8], 2)
            b = int(instruction_root[8::], 2)

            if opcode == "00101":
                st(a, b)
            if opcode == "00100":
                ld(a, b)

        elif interpreted == 'E':
            # if len(instruct_root)!=2:
            #     print("ERROR: Incorrect number of operands provided.")
            #     quit()
            # if instruct_root[1] not in labels:
            #     print("Definition Error:  Label '" + instruct_root_p[1] + "' not Defined")
            #     quit()
                #raise Exception("Definition Error:  Label '" + instruct_root_p[1] + "' not Defined")

            # mac_code+=labels[instruct_root[1]]
            a = int(instruction_root[8::], 2)
            if opcode == "01111":
                jmp(a)
                return
            if opcode == "10000":
                jlt(a)
                return
            if opcode == "10001":
                jgt(a)
                return
            if opcode == "10010":
                je(a)
                return


        elif interpreted == 'F':
            check = 1
        # mac_code += "\n"
        if check == 1:
            return
    print(AddressFiller(instruction_root_index), end=" ")
    for reg in registers_display:
        print(reg, end= " ")
    print(('0'*12)+V+L+G+E) """


def execute(program_counter):
    global cycle, points_x, points_y
    global check, memory, memory_dis, registers, registers_display, V, L, G, E
    halted = False
    instruction_root = memory_dis[program_counter]
    opcode = instruction_root[:5:]
    interpreted = operations.get(opcode)
    if interpreted == "A":
        resetFlags()
        a = int(instruction_root[7:10:], 2)
        b = int(instruction_root[10:13:], 2)
        c = int(instruction_root[13::], 2)
        if opcode == '00000':
            add(a, b, c)

        if opcode == '00001':
            sub(a, b, c)

        if opcode == '00110':
            mul(a, b, c)

        if opcode == '01010':
            eor(a, b, c)

        if opcode == '01011':
            orr(a, b, c)

        if opcode == '01100':
            annd(a, b, c)
        program_counter += 1

    elif interpreted == 'B':
        resetFlags()
        a = int(instruction_root[5:8:], 2)
        b = int(instruction_root[8::], 2)
        if opcode == "00010":
            mov_im(a, b)

        if opcode == "01000":
            rs(a, b)

        if opcode == "01001":
            ls(a, b)

        program_counter += 1

    elif interpreted == 'C':
        a = int(instruction_root[10:13:], 2)
        b = int(instruction_root[13::], 2)
        if opcode == '00011':
            if b == 7:
                mov_f(a)
            else:
                mov(a, b)

        resetFlags()

        if opcode == '00111':
            div(a, b)

        if opcode == '01101':
            nott(a, b)

        if opcode == '01110':
            cmp(a, b)

        program_counter += 1

    elif interpreted == 'D':
        a = int(instruction_root[5:8], 2)
        b = int(instruction_root[8::], 2)

        if opcode == "00101":
            points_x.append(cycle)
            points_y.append(b)
            st(a, b)
        if opcode == "00100":
            points_x.append(cycle)
            points_y.append(b)
            ld(a, b)

        program_counter += 1
        resetFlags()

    elif interpreted == 'E':
        a = int(instruction_root[8::], 2)
        if opcode == "01111":
            program_counter = jmp(a)
        if opcode == "10000":
            program_counter = jlt(a, program_counter)
        if opcode == "10001":
            program_counter = jgt(a, program_counter)
        if opcode == "10010":
            program_counter = je(a, program_counter)
        resetFlags()

    elif interpreted == 'F':
        program_counter += 1
        halted = True

    return halted, program_counter


def main():
    global cycle, points_x, points_y, pc, V, L, G, E, memory_dis
    halted = False

    cycle = 0
    points_x = []
    points_y = []
    pc = 0
    while(not halted):
        points_x.append(cycle)
        points_y.append(pc)
        halted, new_PC = execute(pc)
        print(AddressFiller(pc), end=" ")
        for reg in registers_display:
            print(reg, end=" ")
        print(('0'*12)+V+L+G+E)
        pc = new_PC
        cycle += 1

    plt.scatter(points_x, points_y)
    plt.title("Memory Accesses v/s Cycles")
    plt.ylabel("Address")
    plt.xlabel("Cycle")
    plt.savefig('plot.png')
    
    for mem in memory_dis:
        print(mem)

main()
