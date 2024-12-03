import re
from functools import reduce
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_muls(s):
    mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
    muls = re.findall(mul_pattern, s)
    operands_pattern = r"\d+"
    return map(lambda mul: map(int, re.findall(operands_pattern, mul)), muls)

def get_muls_with_conds(s):
    mul_conds_pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    matches = re.findall(mul_conds_pattern, s)
    include_mul = True
    do_prefix = "do"
    dont_prefix = "don't"
    included_muls = list()
    for op in matches:
        if (op.startswith(dont_prefix)):
            include_mul = False
        elif (op.startswith(do_prefix)):
            include_mul = True
        elif (include_mul):
            included_muls.append(op)
    operands_pattern = r"\d+"
    return map(lambda mul: map(int, re.findall(operands_pattern, mul)), included_muls)

def main():
    content = read_file("3.in")
    #muls = get_muls(content)
    muls = get_muls_with_conds(content)
    results = map(lambda mul: reduce(lambda x, y: (x * y), mul), muls)
    return sum(results)

if __name__ == "__main__":
    result = main()
    print(result)
