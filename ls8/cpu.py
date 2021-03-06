"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b1000101
POP = 0b01000110

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # open the file
        with open(filename) as my_file:
            # go through each line to parse and get the instruction
            for line in my_file:
                # try and get the instruction/operand in the line
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]

                # wrap in a try/except block in case not a binary number
                try:
                    # save to x a binary number, base 2
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    print("oops, error")
                    # or could just put 'continue'



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        if op == MUL:
            self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
            self.pc += 3
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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1

        elif instruction == PRN:
            print(self.registers[operand_a])
            self.pc += 2

        elif instruction == LDI:
            self.registers[operand_a] = operand_b
            self.pc += 3

        elif instruction == MUL:
            # if doing by alu
            self.alu(instruction, operand_a, operand_b)

            # # if not doing by alu but by execute_instruction
            # self.registers[operand_a] = self.registers[operand_a] * self.registers[operand_b]
            # self.pc += 3

        elif instruction == PUSH:
            # 1. decrement the stack pointer
            self.registers[SP] -= 1

            # 2. store the operand in the stack
            self.ram_write(self.registers[operand_a], self.registers[SP])
            self.pc += 2

        elif instruction == POP:
            self.registers[operand_a] = self.ram_read(self.registers[SP])
            self.registers[SP] += 1
            self.pc += 2

        else:
            print("idk what to do.")
            pass