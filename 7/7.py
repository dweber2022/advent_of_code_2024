from aoclib import parse
from multiprocessing import Pool
from os import cpu_count
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def clean_equation(equation):
    equation[0] = equation[0][:-1]
    return list(map(int, equation))

def is_valid_equation(equation, use_concat=False):
    result = equation[0]
    operands = equation[1:]
    ADD = "+"
    MULTIPLY = "*"
    CONCATENATE = "||"
    if (use_concat):
        OPERATORS = (ADD, MULTIPLY, CONCATENATE)
    else:
        OPERATORS = (ADD, MULTIPLY)
    num_operators = (len(operands) - 1)
    operator_combinations = it.product(OPERATORS, repeat=num_operators)
    for combo in operator_combinations:
        cur_result = operands[0]
        operand_p = 1
        operator_p = 0
        while (operand_p < len(operands)):
            operand = operands[operand_p]
            operator = combo[operator_p]
            if (operator == ADD):
                cur_result += operand
            elif (operator == MULTIPLY):
                cur_result *= operand 
            elif (operator == CONCATENATE):
                cur_result = int(f"{cur_result}{operand}")
            operand_p += 1
            operator_p += 1
        if (result == cur_result):
            return True
    return False

def part1(filename):
    content = read_file(filename)
    equations = parse.parse_matrix(content)
    equations = [clean_equation(equation) for equation in equations]
    correct_equations = filter(is_valid_equation, equations)
    return sum([equation[0] for equation in correct_equations])

def part2(filename):
    content = read_file(filename)
    equations = parse.parse_matrix(content)
    equations = [clean_equation(equation) for equation in equations]
    with Pool(cpu_count()) as p:
        equation_results = p.map(ft.partial(is_valid_equation, use_concat=True), equations)
    correct_equations = map(lambda payload: payload[0], filter(lambda payload: payload[1], zip(equations, equation_results)))
    return sum([equation[0] for equation in correct_equations])

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
        out = 3749
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 11387
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "7"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
