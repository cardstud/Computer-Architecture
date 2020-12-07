"""CPU functionality."""

import sys
from datetime import datetime

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0,0,0,0,0,0,0,0]
        self.running = False
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.IS = 6
        self.reg[self.IS] = 0b00000000
        self.IM = 5
        self.reg[self.IM] = 0b00000000
        self.fl = 4
        self.reg[self.fl] = 0b00000000
        self.time = int(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:])
        self.branch_table = {}
        self.branch_table[0b10000010] = self.LDI
        self.branch_table[0b01000111] = self.PRN
        self.branch_table[0b00000001] = self.HLT
        self.branch_table[0b10100000] = self.ADD
        self.branch_table[0b10100010] = self.MUL
        self.branch_table[0b01000101] = self.PUSH
        self.branch_table[0b01000110] = self.POP
        self.branch_table[0b01010000] = self.CALL
        self.branch_table[0b00010001] = self.RET
        self.branch_table[0b10100111] = self.CMP
        self.branch_table[0b01010100] = self.JMP
        self.branch_table[0b01010101] = self.JEQ
        self.branch_table[0b01010110] = self.JNE
        self.branch_table[0b10000100] = self.ST
        self.branch_table[0b01001000] = self.PRA
        self.branch_table[0b00010011] = self.IRET
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def LDI(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN(self):
        operand_a = self.ram[self.pc + 1]
        print(self.reg[operand_a])
        self.pc += 2

    def HLT(self):
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        self.running = True
    
        while self.running:
            if int(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:]) == self.time + 1:
                self.reg[self.IS] = 0b00000001

            elif bin(self.reg[self.IS]) == '0b1' :
                masked_interrupts = self.reg[self.IM] & self.reg[self.IS]

                for i in range(8):
                    interrupt_happened = ((masked_interrupts >> i) & 1) == 1
                    if interrupt_happened:
                        self.reg[self.IS] = 0b00000000
                        self.ram[self.reg[self.sp]] = self.pc
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[self.fl]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[0]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[1]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[2]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[3]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[4]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[5]
                        self.reg[self.sp] -= 1
                        self.ram[self.reg[self.sp]] = self.reg[6]
                        self.pc = self.ram[0xf8]

                continue

            else:
                IR = self.ram[self.pc]
                # print(bin(IR))
    
                if IR in self.branch_table:
                    # print(self.branch_table[self.ram[self.pc]])
                    self.branch_table[IR]()

                else:
                    print(f'unknown command {IR}')
                    self.running = False
