from aoclib import parse
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class Machine:
    A_cost = 3
    B_cost = 1

    def __init__(self, desc):
        self.A = self.parse_pos(desc[0])
        self.B = self.parse_pos(desc[1])
        self.prize = self.parse_pos(desc[2])
    
    def parse_pos(self, desc):
        pos = desc.split()[-2:]
        x = int(pos[0][2:-1])
        y = int(pos[1][2:])
        return (x, y)

    def __str__(self):
        return f"A: {self.A}, B: {self.B}, Prize: {self.prize}"

def get_inputs_to_prize(machine, input_limit):
    # Solve for two unknowns using two equations
    A = machine.A
    B = machine.B
    prize = list(machine.prize)
    prize[1] -= (B[1] * prize[0] / B[0])
    ratio_B_to_A = (-A[0] / B[0])
    num_A_inputs = round(prize[1] / (A[1] + (B[1] * ratio_B_to_A)))
    num_B_inputs = round((prize[0] - (A[0] * num_A_inputs)) / B[0])
    if (
        (num_A_inputs <= input_limit) and
        (num_B_inputs <= input_limit) and
        ((A[0] * num_A_inputs) + (B[0] * num_B_inputs) == machine.prize[0]) and
        ((A[1] * num_A_inputs) + (B[1] * num_B_inputs) == machine.prize[1]) 
    ):
        return (num_A_inputs, num_B_inputs)
    else:
        return (-1, -1)

def part1(filename):
    content = read_file(filename)
    machines = [Machine(m) for m in parse.parse_matrix(content, col_delim="\n", row_delim="\n\n")]
    input_limit = 100
    inputs_to_prizes = map(ft.partial(get_inputs_to_prize, input_limit=input_limit), machines)
    inputs_to_prizes = filter(lambda inputs: (inputs != (-1, -1)), inputs_to_prizes)
    total_cost = sum(map(lambda inputs: ((Machine.A_cost * inputs[0]) + (Machine.B_cost * inputs[1])), inputs_to_prizes))
    return total_cost

def part2(filename):
    content = read_file(filename)
    machines = [Machine(m) for m in parse.parse_matrix(content, col_delim="\n", row_delim="\n\n")]
    for machine in machines:
        machine.prize = (machine.prize[0]+10000000000000, machine.prize[1]+10000000000000)
    input_limit = float("inf")
    inputs_to_prizes = map(ft.partial(get_inputs_to_prize, input_limit=input_limit), machines)
    inputs_to_prizes = filter(lambda inputs: (inputs != (-1, -1)), inputs_to_prizes)
    total_cost = sum(map(lambda inputs: ((Machine.A_cost * inputs[0]) + (Machine.B_cost * inputs[1])), inputs_to_prizes))
    return total_cost


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
        out = 480
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = None
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "13"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
