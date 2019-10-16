"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    # Add the constructor to cpu.py
    # Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers.
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0     # added pc starting value here so just in case other methods need it
        self.ram = [0] * 256
        self.reg = [0] * 8

    # Add RAM functions 
    # ram_read() should accept the address to read and return the value stored there.
    # raw_write() should accept a value to write, and the address to write it to.
    def ram_read(self, ram_address):
        return self.ram[ram_address]

    def ram_write(self, ram_write, ram_address):
        self.ram[ram_address] = ram_write

    def load(self, program):
        """Load a program into memory."""

        
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    comment_split = line.split("#")
                
                    num = comment_split[0].strip()
                
                    try:
                        self.ram_write(int(num, 2), address)
                        address += 1
                    except ValueError:
                        continue

            print("self.ram: ", self.ram)
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # program = [
        #     # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b10100010,     # MUL next 2 registers
            # 0b00000010,     # 2
            # 0b00000011,     # 3
            # 0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    # read the memory address that's stored in register PC, and store that result in IR, the Instruction Register.
    # perform the actions needed for the instruction per the LS-8 spec. Maybe an if-elif cascade...?
    def run(self):
        """Run the CPU."""
        running = True

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        SP = 7  # points to which register number that holds the address top element of the stack
        self.reg[SP] = len(self.ram) - 1    # initially stack is at the last address in memory

        while running:
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            command = self.ram[self.pc]     # ram contains all instructions to execute, vales to read and write, etc and uses program counter to keep track of current index location


            if command == HLT:  # ends program
                running = False

            elif command == LDI:
                # int(self.reg[operand_a])
                # self.pc += 1
                print("LDI: Loaded registerA with the value at the memory address stored in registerB.")
                self.reg[operand_a] = operand_b
                print(f"LDI: {self.reg[operand_a]}")
                self.pc += 3

            elif command == MUL:
                print("Mul: registerA * registerB and store value in registerA.")
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif command == PRN:
                print(f"PRN: {self.reg[operand_a]}")
                self.pc += 2

            elif command == PUSH:
                print("Push the value in the given register on the stack")
                reg_number = self.ram[self.pc + 1]
                reg_val = self.reg[reg_number]
                self.reg[SP] -= 1  # Decrement SP
                self.ram[self.reg[SP]] = reg_val
                self.pc += 2

            elif command == POP:
                print("Pop the value from the top of the stack and store it in the PC")
                reg_number = self.ram[self.pc + 1]
                reg_val = self.ram[self.reg[SP]]
                self.reg[reg_number] = reg_val
                self.reg[SP] += 1
                self.pc += 2