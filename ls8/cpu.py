"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 7
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP

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
        else:
            raise Exception("Unsupported ALU operation")

    def handle_HLT(self):
        sys.exit()
    
    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self, operand_a):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                # print("HALTING")
                self.branchtable[HLT]()
            elif IR == LDI:
                # print(f"LDA ADDRESS: {operand_a} VALUE: {operand_b}")
                self.branchtable[LDI](operand_a, operand_b)
            elif IR == PRN:
                # print("PRINTING")
                self.branchtable[PRN](operand_a)
            elif IR == MUL:
                # print("MULTIPLYING")
                self.branchtable[MUL](operand_a, operand_b)
            elif IR == PUSH:
                # print("PUSHING")
                self.branchtable[PUSH](operand_a)
            elif IR == POP:
                # print("POPPING")
                self.branchtable[POP](operand_a)
            else:
                print(f"INVALID INSTRUCTION {IR}")
                running = False

