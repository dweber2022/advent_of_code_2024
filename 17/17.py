from aoclib import parse
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class Computer:
    def __init__(self, registers, program):
        self.registers = self.parse_registers(registers)
        self.program = self.parse_program(program)
        self.instructions = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        self.ip = 0
        self.out_buffer = list()

    def reg_A(self):
        return self.registers[0]

    def set_A(self, val):
        self.registers[0] = val

    def reg_B(self):
        return self.registers[1]

    def set_B(self, val):
        self.registers[1] = val

    def reg_C(self):
        return self.registers[2]

    def set_C(self, val):
        self.registers[2] = val

    def get_ip(self):
        return self.ip 

    def set_ip(self, addr):
        self.ip = addr

    def get_combo_operand_value(self, operand):
        if (0 <= operand <= 3):
            return operand
        elif (operand == 4):
            return self.reg_A()
        elif (operand == 5):
            return self.reg_B()
        elif (operand == 6):
            return self.reg_C()

    def clear_output_buffer(self):
        self.out_buffer = list()

    def run_program(self, print_state=False):
        self.clear_output_buffer()
        self.set_ip(0)
        while (self.get_ip() < len(self.program)):
            if (print_state):
                self.print_state()
            opcode = self.program[self.get_ip()]
            if ((self.get_ip() + 1) < len(self.program)):
                operand = self.program[self.get_ip()+1]
            else:
                operand = None
            instruction = self.opcode_to_instruction(opcode)
            cur_ip = self.get_ip()
            instruction(operand)
            if (self.get_ip() != cur_ip):
                continue
            else:
                self.set_ip(self.get_ip()+2)

    def opcode_to_instruction(self, opcode):
        return self.instructions[opcode]

    def adv(self, operand):
        numerator = self.reg_A()
        denominator = (2 ** self.get_combo_operand_value(operand))
        result = (numerator // denominator)
        self.set_A(result)

    def bxl(self, operand):
        result = (self.reg_B() ^ operand)
        self.set_B(result)

    def bst(self, operand):
        value = self.get_combo_operand_value(operand)
        result = ((value % 8) & (2 ** 3 - 1))
        self.set_B(result)

    def jnz(self, operand):
        if (self.reg_A() == 0):
            return
        else:
            self.set_ip(operand)

    def bxc(self, _):
        result = (self.reg_B() ^ self.reg_C())
        self.set_B(result)

    def out(self, operand):
        value = self.get_combo_operand_value(operand)
        result = (value % 8)
        self.out_buffer.append(result)

    def bdv(self, operand):
        numerator = self.reg_A()
        denominator = (2 ** self.get_combo_operand_value(operand))
        result = (numerator // denominator)
        self.set_B(result)

    def cdv(self, operand):
        numerator = self.reg_A()
        denominator = (2 ** self.get_combo_operand_value(operand))
        result = (numerator // denominator)
        self.set_C(result)

    def parse_registers(self, registers):
        registers = [int(r.split()[-1]) for r in registers]
        return registers

    def parse_program(self, program):
        program = program[0].split()[-1]
        program = [int(n) for n in program.split(",")]
        return program

    def print_state(self):
        INSTRUCTION_TO_NAME = {
            self.adv: "adv",
            self.bxl: "bxl",
            self.bst: "bst",
            self.jnz: "jnz",
            self.bxc: "bxc",
            self.out: "out",
            self.bdv: "bdv",
            self.cdv: "cdv"
        }
        instruction = self.opcode_to_instruction(self.program[self.get_ip()])
        if (self.get_ip() < len(self.program)):
            operand = self.program[self.get_ip()+1]
        state = f"""
            REGISTERS: {self.registers}
            IP: {self.get_ip()}
            INST|OPERAND: {INSTRUCTION_TO_NAME[instruction]}|{operand}
        """
        pprint(state)

def part1(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, col_delim="\n", row_delim="\n\n")
    registers = payload[0]
    program = payload[1]
    computer = Computer(registers, program)
    computer.run_program()
    output = computer.out_buffer
    return ",".join([str(c) for c in output])

def find_min_A_for_length(computer):
    A = 0
    computer.set_A(A)
    program = computer.program
    computer.run_program()
    mult = 1
    while (len(computer.out_buffer) < len(program)):
        A = (1 << (3 * mult))
        mult += 1
        computer.set_A(A)
        computer.run_program()
    return A

def find_A_for_quine(computer):
    A_min = find_min_A_for_length(computer)
    A_max = ((A_min << 3) - 1)

    @ft.cache
    def dfs(A, match_idx=0):
        computer.set_A(A)
        computer.run_program()
        if (
            (match_idx != 0) and
            (computer.out_buffer[-match_idx] != computer.program[-match_idx])
        ):
            return
        if (match_idx == len(computer.program)):
            return A
        num_chunks = (3 * (len(computer.program) - match_idx))
        A_base = A
        for offset in range(2 ** 3):
            offset <<= (num_chunks - 3)
            A_offset = (A_base + offset)
            result = dfs(A_offset, match_idx+1)
            if (result is not None):
                return result

    return dfs(A_min)

def part2(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, col_delim="\n", row_delim="\n\n")
    registers = payload[0]
    program = payload[1]
    computer = Computer(registers, program)
    return find_A_for_quine(computer)

def main(filename):
    return (
        part1(filename),
        part2(filename)
    )

class Test(unittest.TestCase):
    filename = ""

    @staticmethod
    def set_filename(filename):
        Test.filename = filename

    def test_1_small(self):
        out = "4,6,3,5,6,3,5,2,1,0"
        self.assertEqual(part1("17.small1.in"), out)

    def test_2_small(self):
        out = 117440
        self.assertEqual(part2("17.small2.in"), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "17"
    filename = f"{day}.in"
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
