"""CPU functionality."""
#python3 ls8.py sctest.ls8

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # allocate 256 bytes of memory
        self.pc = 0
        self.reg = [0] * 8
        self.fl  = 0
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010
        self.MUL = 0b10100010
        self.POP = 0b01000110
        self.PUSH= 0b01000101
        self.CALL= 0b01010000
        self.RET = 0b00010001
        self.sp  = 0xf4
        self.CMP = 0b10100111
        self.E   = 0
        self.L   = 0
        self.G   = 0
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110



    def ram_read(self, MAR):
        value = self.ram[MAR]
        return value

    def ram_write(self, address, MDR):
        self.ram[address] = MDR

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
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        prog = sys.argv[1]

        with open(prog) as f:
            for line in f:
                # print(line)
                line = line.split("#")[0]
                # print(f" first exe {line}")
                line = line.strip() # lose whitespace
                # print(f" second exe {line}")

                if line == "":
                    continue

                val = int(line, 2) # LS-8 uses base 2!
                # print(val)

                self.ram[address] = val
                address +=1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == self.CMP:
            if self.reg[reg_a] == self.reg[reg_b]:

                self.E = 1
                self.L = 0
                self.G = 0

            elif self.reg[reg_a] <= self.reg[reg_b]:

                self.E = 0
                self.L = 1
                self.G = 0

            else:

                self.E = 0
                self.L = 0
                self.G = 1

        else:
            raise Exception("Unsupported ALU operation")

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
        halted = False

        while not halted:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.LDI:
                # Set the value of a register to an integer.
                register_index = operand_a
                self.reg[register_index] = operand_b
                self.pc += 3
                # print("pass")
            # elif IR == OPCODES.NOP.code:
            #     self.pc += 1
            elif IR == self.PRN:
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given
                # register.
                reg_index = operand_a
                value = int(self.reg[reg_index])
                print(f'{value}')
                self.pc += 2

            elif IR == self.HLT:
                halted = True


            elif IR == self.MUL:
                self.alu(self.MUL, operand_a, operand_b)
                self.pc += 3

            elif IR == self.POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp + 1)
                self.pc += 2

            elif IR == self.PUSH:
                self.sp = (self.sp - 1)
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2

            elif IR == self.CMP:
                self.alu(self.CMP, operand_a, operand_b)
                self.pc += 3

            elif IR == self.JMP:
                self.pc = self.reg[operand_a]

            elif IR == self.JEQ:
               if self.E == 1:
                   self.pc = self.reg[operand_a]
               else:
                   self.pc += 2

            elif IR == self.JNE:
               if self.E == 0:
                   self.pc = self.reg[operand_a]
               else:
                   self.pc += 2

            else:
                print(f'Unknown instruction at index {self.pc}')
                self.pc += 1