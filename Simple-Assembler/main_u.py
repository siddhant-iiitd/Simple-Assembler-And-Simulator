#Simple Assembler Q1. COA Assignment
#Assumptions:
#1. We have considered all the inputs to the program to be case-insensitive just like in the actual asssembly language.
#   eg:- Mov r1 Flags is equivalent to mov R1 FLAGS,etc.
#
#2. We have taken the input via stdin using 'stdin' from 'sys' library, and given the output in stdout.

from sys import stdin
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
global linec
linec=0
quiting=0
try:
    quiting=1
    operations = {'add':('00000', 'A'), 'sub':('00001', 'A'), 'mov_im':('00010', 'B'), 'mov':('00011', 'C'), 'mov_f':('00011', 'C'), 'ld':('00100', 'D'),
                  'st': ('00101', 'D'),'mul':('00110', 'A'), 'div':('00111', 'C'), 'rs':('01000', 'B'), 'ls':('01001', 'B'),
                  'xor':('01010', 'A'), 'or':('01011', 'A'), 'and':('01100', 'A'), 'not': ('01101', 'C'), 'cmp': ('01110', 'C'),
                  'jmp': ('01111', 'E'), 'jlt': ('10000', 'E'), 'jgt': ('10001', 'E'), 'je': ('10010', 'E'), 'hlt':('10011', 'F')}#changed

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

    def BFiller(a): #changed
        b = str(bin(a))[2::]
        b = "0"*(16-len(b))+b
        #b = "0"*(16-len(b[-8:]))+b[-8:] #use for overflow handling
        return b

    def AddressFiller(a):
        b = str(bin(a))[2::]
        b = "0" * (8 - len(b)) + b
        return b

    #flagRegister = [0]*16 #changed
    global V, L, G, E
    V = "0"
    G = "0"
    L = "0"
    E = "0"

    def add(a, b, c): #changed
        global V
        V="0"
        if((registers[b] + registers[c])>255 or (registers[b] + registers[c])<0):
            V="1"
        registers[a] = registers[b] + registers[c]
        if V=="1":
            c=registers[a]//256
            registers[a]-=(256*c)
            #registers[a]=registers[a]%256
        registers_display[a] = BFiller(registers[a])

    def sub(a, b, c): #changed
        global V
        V="0"
        if(registers[b]<registers[c]):
            V="1"
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

    def mov_f(a, b): #changed
        registers[a] = b
        registers_display[a] = BFiller(registers[a])

    def ld(a, b):
        registers[a] = memory[b]
        registers_display[a] = memory_dis[b]

    def st(a, b):
        memory[b] = registers[a]
        memory_dis[b] = registers_display[a]

    def mul(a, b, c): #changed
        global V
        V="0"
        if((registers[b] * registers[c])>255 or (registers[b] * registers[c])<0):
            V="1"
        registers[a] = registers[b] * registers[c]
        if V=="1":
            c=registers[a]//256
            registers[a]-=(256*c)
        registers_display[a] = BFiller(registers[a])

    def div(b, c):
        # if(registers[c]==0):
        #     print("ERROR @Line "+str(linec)+": Divison by zero error")
        #     quit()
        if(registers[c]!=0):
            registers[0] = registers[b]//registers[c]
            registers_display[0] = BFiller(registers[0])
            registers[1] = registers[b]%registers[c]
            registers_display[1] = BFiller(registers[1])

    def rs(a, imm):
        if imm>=16:
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
        registers[a] = registers[c]^registers[b]
        registers_display[a] = BFiller(registers[a])
    def orr(a, b, c):
        registers[a] = registers[c]|registers[b]
        registers_display[a] = BFiller(registers[a])
    def annd(a, b, c):
        registers[a] = registers[c]&registers[b]
        registers_display[a] = BFiller(registers[a])
    def nott(a, b):
        registers[a] = ~registers[b]
        registers_display[a] = BFiller(registers[a])
    def cmp(a, b):
        global V, L, G, E
        G = "0"
        L = "0"
        E = "0"
        if a>b:
            G = "1"
        if a == b:
            E = "1"
        if a < b:
            L = "1"
    def jmp(a):
        # hlt()
        # code.seek(int(a, 2), 0)
        pass

    def jlt(a):
        if (L == "1"):
            jmp(a)
    def jgt(a):
        if (G == "1"):
            jmp(a)
    def je(a):
        if (E == "1"):
            jmp(a)
    def hlt():
        quit()


    type = {'A':(2, 3, 3, 3, 0), 'B':(0, 3, 0, 0, 8), 'C':(5, 3, 3, 0, 0), 'D':(0, 3, 0, 0, 8), 'E':(3, 0, 0, 0, 8), 'F':(11, 0, 0, 0, 0)}
    # 0th-> unused,reg1, reg2, reg3, mem/imm.
    # code = open('test.txt', 'r') #changed
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
    # code for var....-> using prepocessor loop(till instruct_root  == var....append lines of code to a str s...

    global instruct_root_p
    vcount = 0
    vflag = 0
    hlt_c = 0
    global Ninstr
    #global linec
    for preprocessor in code.splitlines(): #for preprocessor in code.readlines():  #changed
        #global linec
        linec+=1
        if preprocessor == "\n" or preprocessor == '':
            continue
        if (hlt_c>0):
            print("ERROR @Line "+str(linec)+": Misplaced halt statements(hlt is not the last instruction and is followed by other code line/s. Also, hlt should only be declared once)")
            quit()
        instruct_root_p = preprocessor.split()
        if (instruct_root_p[0].lower()=='hlt' and len(instruct_root_p)==1) or (instruct_root_p[0][-1]==':' and len(instruct_root_p)==2 and instruct_root_p[1].lower()=='hlt'):
            hlt_c+=1
        if instruct_root_p[0].lower() == "var":
            if vflag==1:
                print("ERROR @Line "+str(linec)+": Declare variables only at the top")
                quit()
            if len(instruct_root_p)!=2:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            if instruct_root_p[1].upper() in ["FLAGS","R0","R1","R2","R3","R4","R5","R6"] or instruct_root_p[1].lower() in operations.keys():
                print("ERROR @Line "+str(linec)+": Illegal use of reserved key words(register name, operation name).")
                quit()
                #raise Exception("Illegal use of reserved key words(register name, operation name).")
            if instruct_root_p[1].lower() in labels.keys():
                print("ERROR @Line "+str(linec)+": Label with given variable name already exists.")
                quit()
                #raise Exception("Label with given variable name already exists.")
            if instruct_root_p[1].lower() in vars.keys():
                print("ERROR @Line "+str(linec)+": Variable with given variable name already exists.")
                quit()
            if instruct_root_p[1] not in vars:
                vars[instruct_root_p[1].lower()] = vcount
                vcount+=1
                continue
        vflag=1
        i+=1
        if instruct_root_p[0][-1] == ":":
            if instruct_root_p[0][:-1:].upper() in ["FLAGS","R0","R1","R2","R3","R4","R5","R6"] or instruct_root_p[0][:-1:].lower() in operations.keys():
                print("ERROR @Line "+str(linec)+": Illegal use of reserved key words(register name, operation name).")
                quit()
                #raise Exception("Illegal use of reserved key words(register name, operation name).")
            if instruct_root_p[0][:-1:].lower() in vars.keys():
                print("ERROR @Line "+str(linec)+": Variable with given label name already exists.")
                quit()
                #raise Exception("Variable with given label name already exists.")
            if len(instruct_root_p)==1:    #ask doubt for empty labels
                print("ERROR @Line "+str(linec)+": Label not defined(Empty Label given)")
                quit()
            for member in instruct_root_p[0][:-1:].lower():
                if not(member.isalnum()) and not(member=='_'):
                    print("ERROR @Line "+str(linec)+": Label name can only contain alphanumeric or '_' characters")
                    quit()
            if instruct_root_p[0][:-1:].lower() in labels.keys():
                print("ERROR @Line "+str(linec)+": Label with given lable name already exists.")
                quit()
            else:
                labels[instruct_root_p[0][:-1:].lower()] = AddressFiller(i-1)

        Ninstr = i

    if(hlt_c>1):
        print("ERROR: Multiple hlt statements declared")
        quit()

    #if instruct_root_p[0] != "hlt": #changed
    if ((instruct_root_p[0].lower()!="hlt" and len(instruct_root_p)==1) or (instruct_root_p[0][-1]==':' and len(instruct_root_p)==2 and instruct_root_p[1].lower()!='hlt')):
        print("ERROR: No exit statement(hlt) in code.")
        quit()
    if len(instruct_root_p)>2:
        print("ERROR @Line "+str(linec)+": Incorrect/Absent hlt declaration")
        quit()
    # if instruct_root_p[-1] != "hlt":
    #     print("ERROR: No exit statement(hlt) in code.")
    #     quit()
        #raise Exception("No exit statement in code.")

    for i in vars.keys():
        vars[i] = AddressFiller(Ninstr + vars[i])

    linec=0
    #code.seek(0, 0)#change if file input not req. #changed
    pc = 0
    for instruction in code.splitlines(): #for instruction in code.readlines():  #changed
        #global linec
        linec+=1
        if instruction == "\n" or instruction == '':
            continue
        pc+=1
        instruct_root = instruction.split()

        if instruct_root[0][0:2] == "//" or instruct_root[0].lower() == "var":
            continue
        if instruct_root[0][-1] == ":":
            instruct_root.pop(0)
        if instruct_root[0].lower() not in operations or instruct_root[0].lower()=="mov_im" or instruct_root[0].lower()=="mov_f":
            print("ERROR @Line "+str(linec)+": "+instruct_root[0] + " is not a valid command")
            quit()
            #raise Exception(instruct_root[0] + " is not a valid command")
        if instruct_root[0].lower() == "mov" and len(instruct_root)==3 and instruct_root[2][0] == "$":
            if(len(instruct_root[2])==1):
                print("ERROR @Line "+str(linec)+": Immediate Value not specified")
                quit()
            try:
                int(instruct_root[2][1:])
                if(int(instruct_root[2][1:])!=float(instruct_root[2][1:])):
                    print("ERROR @Line "+str(linec)+": Immediate Value can't be a floating point number")
                    quit()
            except:
                print("ERROR @Line "+str(linec)+": Immediate Value given is not valid ")
                quit()
            instruct_root[0] = "mov_im"
        if instruct_root[0].lower() == "mov" and len(instruct_root)==3 and instruct_root[2].upper() == "FLAGS":
            instruct_root[0] = "mov_f"

        if(instruct_root[0].lower() not in operations.keys()):
            print("ERROR @Line "+str(linec)+": Illegal operation name used ")
            quit()
            #raise Exception("Illegal operation name used ")
        interpreted = operations.get(instruct_root[0].lower())

        mac_code += interpreted[0]
        mac_code += "0" * type.get(interpreted[1])[0]
        lf=0
        if interpreted[1] != 'C' and instruct_root[0] != "mov_f":
            for s in instruct_root:
                if(s.upper()=="FLAGS"):
                    lf=1
                    break
            if(lf==1):
                print("ERROR @Line "+str(linec)+": Illegal use of FLAGS register")
                quit()
                #raise Exception("Illegal use of FLAGS register")

        if interpreted[1] == 'A':
            if len(instruct_root)!=4:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            r_names=["R0","R1","R2","R3","R4","R5","R6"]
            if (instruct_root[1].upper() == "FLAGS" or instruct_root[2].upper() == "FLAGS" or instruct_root[3].upper() == "FLAGS"):
                print("ERROR @Line "+str(linec)+": Illegal use of FLAGS register")
                quit()
            if (instruct_root[1].upper() not in r_names or instruct_root[2].upper() not in r_names or instruct_root[3].upper() not in r_names):
                print("ERROR @Line "+str(linec)+": Illegal register name used")
                quit()
                #raise Exception("Illegal register name used")
            mac_code+=Rfiller(int(instruct_root[1][1::]))
            mac_code+=Rfiller(int(instruct_root[2][1::]))
            mac_code+=Rfiller(int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'add':
                add(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'sub':
                sub(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'mul':
                mul(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'xor':
                eor(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'or':
                orr(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))

            if instruct_root[0].lower() == 'and':
                annd(int(instruct_root[1][1::]), int(instruct_root[2][1::]), int(instruct_root[3][1::]))


        elif interpreted[1] == 'B' : #changed
            if len(instruct_root)!=3:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            r_names=["R0","R1","R2","R3","R4","R5","R6"]
            if (instruct_root[1].upper() == "FLAGS"):
                print("ERROR @Line "+str(linec)+": Illegal use of FLAGS register")
                quit()
            if (instruct_root[1].upper() not in r_names):
                print("ERROR @Line "+str(linec)+": Illegal register name used")
                quit()
                #raise Exception("Illegal register names used")
            if (int(instruct_root[2][1::])>255 or int(instruct_root[2][1::])<0):
                print("ERROR @Line "+str(linec)+": Illegal Immediate values")
                quit()
                #raise Exception("Illegal Immediate values")

            mac_code+=Rfiller(int(instruct_root[1][1::]))
            mac_code+=MIfiller(int(instruct_root[2][1::]))

            if instruct_root[0].lower() == "mov_im":
                mov_im(int(instruct_root[1][1::]), int(instruct_root[2][1::]))

            if instruct_root[0].lower() == "rs":
                rs(int(instruct_root[1][1::]),int(instruct_root[2][1::]))

            if instruct_root[0].lower() == "ls":
                ls(int(instruct_root[1][1::]),int(instruct_root[2][1::]))

        elif instruct_root[0] == "mov_f" and interpreted[1] == 'C': #changed
                if len(instruct_root)!=3:
                    print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                    quit()
                r_names=["R0","R1","R2","R3","R4","R5","R6"]
                if (instruct_root[1].upper() not in r_names):
                    print("ERROR @Line "+str(linec)+": Illegal register name used")
                    quit()
                    #raise Exception("Illegal register names used")
                mac_code+=Rfiller(int(instruct_root[1][1::]))
                #mac_code+=MIfiller(int((8*int(V))+(4*int(L))+(2*int(G))+int(E))) #or we can make it like a regular mov with 2 regs by putting in address of FLAGS reg as 111
                mac_code+='111'
                mov_f(int(instruct_root[1][1::]), int('0'*12+V+L+G+E,2))#((8*int(V))+(4*int(L))+(2*int(G))+int(E))


        elif interpreted[1] == 'C' and instruct_root[0] != "mov_f":
            if len(instruct_root)!=3:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            r_names=["R0","R1","R2","R3","R4","R5","R6"]
            if (instruct_root[1].upper() == "FLAGS"):
                print("ERROR @Line "+str(linec)+": Illegal use of FLAGS register")
                quit()
            if (instruct_root[1].upper() not in r_names or instruct_root[2].upper() not in r_names):
                print("ERROR @Line "+str(linec)+": Illegal register name used")
                quit()
                #raise Exception("Illegal register name used")
            mac_code+=Rfiller(int(instruct_root[1][1::]))
            mac_code+=Rfiller(int(instruct_root[2][1::]))

            if instruct_root[0].lower() == 'mov':
                mov(int(instruct_root[1][1::]), int(instruct_root[2][1::]))

            if instruct_root[0].lower() == 'div':
                div(int(instruct_root[1][1::]), int(instruct_root[2][1::]))

            if instruct_root[0].lower() == 'not':
                nott(int(instruct_root[1][1::]), int(instruct_root[2][1::]))

            if instruct_root[0].lower() == 'cmp':
                cmp(int(instruct_root[1][1::]), int(instruct_root[2][1::]))

        elif interpreted[1] == 'D':
            if len(instruct_root)!=3:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            r_names=["R0","R1","R2","R3","R4","R5","R6"]
            if (instruct_root[1].upper() not in r_names):
                print("ERROR @Line "+str(linec)+": Illegal register name used")
                quit()
                #raise Exception("Illegal register name used")
            if (instruct_root[2].upper() in r_names):
                print("ERROR @Line "+str(linec)+": Illegal use of register "+instruct_root[2]+", memory address required")
                quit()
            if instruct_root[2].lower() not in vars:
                print("Definition Error @Line "+str(linec)+":  Variable '" + instruct_root[2] + "' not Defined")
                quit()
                #raise Exception("Definition Error:  Variable '" + instruct_root[2] + "' not Defined")

            mac_code += Rfiller(int(instruct_root[1][1::]))
            mac_code += vars[instruct_root[2].lower()]


            if instruct_root[0].lower() == "st":
                st(int(instruct_root[1][1::]), int(vars[instruct_root[2].lower()], 2))
            if instruct_root[0].lower() == "ld":
                ld(int(instruct_root[1][1::]), int(vars[instruct_root[2].lower()], 2))

        elif interpreted[1] == 'E':
            if len(instruct_root)!=2:
                print("ERROR @Line "+str(linec)+": Incorrect number of operands provided.")
                quit()
            if instruct_root[1].lower() not in labels:
                print("Definition Error @Line "+str(linec)+":  Label '" + instruct_root[1] + "' not Defined")
                quit()
                #raise Exception("Definition Error:  Label '" + instruct_root_p[1] + "' not Defined")

            mac_code+=labels[instruct_root[1].lower()]
            if instruct_root[0].lower() == "jmp":
                jmp(int(labels[instruct_root[1].lower()], 2))
            if instruct_root[0].lower() == "jlt":
                jlt(int(labels[instruct_root[1].lower()], 2))
            if instruct_root[0].lower() == "jgt":
                jgt(int(labels[instruct_root[1].lower()], 2))
            if instruct_root[0].lower() == "je":
                je(int(labels[instruct_root[1].lower()], 2))


        elif interpreted[1] == 'F':
            if len(instruct_root) != 1:
                print("ERROR @Line "+str(linec)+": Invalid hlt Syntax.")
                quit()
            check = 1
        mac_code += "\n"
        if check == 1:
            break

        # print(registers)
        # print(memory)
    print(mac_code)
    # j = 0
    # for i in mac_code.splitlines():
    #     memory_dis[j] = i
    #     j+=1
    #
    # print(labels)
    # print(memory)
    # print(memory_dis)
    # print(((8*int(V))+(4*int(L))+(2*int(G))+int(E))) #changed
    # print(('0'*12)+V+L+G+E)
    # print(registers)
    # print(registers_display)
    # print(labels)
    # print(vars)


except:
    #global linec
    if quiting==0:
        print("ERROR @Line "+str(linec)+": General Synatax Error")
