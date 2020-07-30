"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
ST   = 0b10000100
PRN  = 0b01000111
MUL  = 0b10100010
ADD  = 0b10100000
SUB  = 0b10100001
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
# SPRINT CHALLENGE
CMP  = 0b10100111
JMP  = 0b01010100
JEQ  = 0b01010101
JNE  = 0b01010110

AND  = 0b10101000
OR   = 0b10101010
XOR  = 0b10101011
NOT  = 0b01101001
SHL  = 0b10101100
SHR  = 0b10101101
MOD  = 0b10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 7
        self.fl = [0] * 8
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[ST] = self.handle_ST
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[SUB] = self.handle_SUB
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
# SPRINT CHALLENGE        
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

        self.branchtable[AND] = self.handle_AND
        self.branchtable[OR] = self.handle_OR
        self.branchtable[XOR] = self.handle_XOR
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[MOD] = self.handle_MOD

    def ram_read(self, MAR):
        """Reads and returns value stored in address."""
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        """Writes value to address."""
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(sys.argv[1]) as f:
            for line in f:
                try:
                    str_line = line.split("#")[0].strip()
                    byte = int(str_line, 2)
                    self.ram[address] = byte
                    address += 1
                except:
                    pass

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[7] = 1
            else:
                self.fl[7] = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[5] = 1
            else:
                self.fl[5] = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl[6] = 1
            else:
                self.fl[6] = 0
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print("Cannot divide by 0")
                sys.exit()
            else:
                self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def handle_HLT(self):
        sys.exit()
    
    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_ST(self, operand_a, operand_b):
        self.ram[self.reg[operand_a]] = self.reg[operand_b]
        self.pc += 3

    def handle_PRN(self, operand_a):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def handle_SUB(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)
        self.pc += 3

    def handle_PUSH(self, operand_a):
        self.reg[self.sp] -= 1
        pointer = self.reg[self.sp]
        value = self.reg[operand_a]
        self.ram[pointer] = value
        self.pc += 2

    def handle_POP(self, operand_a):
        pointer = self.reg[self.sp]
        value = self.ram[pointer]
        self.reg[operand_a] = value
        self.reg[self.sp] += 1
        self.pc += 2
    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_CALL(self, operand_a):
        return_address = self.pc + 2

        self.reg[self.sp] -= 1
        pointer = self.reg[self.sp]
        self.ram[pointer] = return_address

        subroutine = self.reg[operand_a]
        self.pc = subroutine

    def handle_RET(self):
        pointer = self.reg[self.sp]
        return_address = self.ram[pointer]
        self.reg[self.sp] += 1

        self.pc = return_address

    # SPRINT CHALLENGE    

    def handle_CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    def handle_JMP(self, operand_a):
        try:
            self.pc = self.reg[operand_a]
        except:
            print("STACK OVERFLOW")
            sys.exit()

    def handle_JEQ(self, operand_a):
        if self.fl[7]:
            print("JEQ-ING TO", self.reg[operand_a], "\n")
            self.pc = self.reg[operand_a]
        else:
            print("JEQ NOTHING HAPPENED\n")
            self.pc += 2

    def handle_JNE(self, operand_a):
        if not self.fl[7]:
            print("JNE-ING TO", self.reg[operand_a], "\n")
            self.pc = self.reg[operand_a]
        else:
            print("JNE NOTHING HAPPENED\n")
            self.pc += 2


    def handle_AND(self, operand_a, operand_b):
        self.alu("AND", operand_a, operand_b)
        self.pc += 3

    def handle_OR(self, operand_a, operand_b):
        self.alu("OR", operand_a, operand_b)
        self.pc += 3

    def handle_XOR(self, operand_a, operand_b):
        self.alu("XOR", operand_a, operand_b)
        self.pc += 3

    def handle_NOT(self, operand_a, operand_b):
        self.alu("NOT", operand_a, operand_b)
        self.pc += 3

    def handle_SHL(self, operand_a, operand_b):
        self.alu("SHL", operand_a, operand_b)
        self.pc += 3

    def handle_SHR(self, operand_a, operand_b):
        self.alu("SHR", operand_a, operand_b)
        self.pc += 3

    def handle_MOD(self, operand_a, operand_b):
        self.alu("MOD", operand_a, operand_b)
        self.pc += 3

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.branchtable[HLT]()
            elif IR == LDI:
                self.branchtable[LDI](operand_a, operand_b)
            elif IR == PRN:
                self.branchtable[PRN](operand_a)
            elif IR == MUL:
                self.branchtable[MUL](operand_a, operand_b)
            elif IR == ADD:
                self.branchtable[ADD](operand_a, operand_b)
            elif IR == SUB:
                self.branchtable[SUB](operand_a, operand_b)
            elif IR == PUSH:
                self.branchtable[PUSH](operand_a)
            elif IR == POP:
                self.branchtable[POP](operand_a)
            elif IR == CALL:
                self.branchtable[CALL](operand_a)
            elif IR == RET:
                self.branchtable[RET]()
# SPRINT CHALLENGE
            elif IR == CMP:
                self.branchtable[CMP](operand_a, operand_b)
            elif IR == JMP:
                self.branchtable[JMP](operand_a)
            elif IR == JEQ:
                self.branchtable[JEQ](operand_a)
            elif IR == JNE:
                self.branchtable[JNE](operand_a)
            elif IR == AND:
                self.branchtable[AND](operand_a, operand_b)
            elif IR == OR:
                self.branchtable[OR](operand_a, operand_b)
            elif IR == XOR:
                self.branchtable[XOR](operand_a, operand_b)
            elif IR == NOT:
                self.branchtable[NOT](operand_a, operand_b)
            elif IR == SHL:
                self.branchtable[SHL](operand_a, operand_b)
            elif IR == SHR:
                self.branchtable[SHR](operand_a, operand_b)
            elif IR == MOD:
                self.branchtable[MOD](operand_a, operand_b)
            else:
                print(f"INVALID INSTRUCTION {IR}")
                running = False

