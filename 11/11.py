from aoclib import parse
from collections import deque
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class DoublyLinkedNode:
    def __init__(self, val):
        self.val = val
        self.before = None
        self.after = None

    def __str__(self):
        return str(self.val)

def construct_dll(l):
    before_root = DoublyLinkedNode(-1)
    root = before_root
    for num in l:
        node = DoublyLinkedNode(num)
        node.before = root
        root.after = node
        root = node
    return before_root.after

def get_num_digits(num):
    if (num == 0):
        return 1
    num_digits = 0
    while (num > 0):
        num_digits += 1
        num //= 10
    return num_digits

def get_digits(num):
    if (num == 0):
        return 0
    digits = deque()
    while (num > 0):
        digit = (num % 10)
        digits.appendleft(digit)
        num //= 10
    return list(digits)

def get_num(digits):
    num = 0
    exp = 0
    rp = (len(digits) - 1)
    while (rp > -1):
        digit = digits[rp]
        num += (digit * (10 ** exp))
        exp += 1
        rp -= 1
    return num

@ft.cache
def get_num_stones_after_blinks(num_blinks, stone_number):
    if (num_blinks <= 0):
        return 1
    if (stone_number == 0):
        return get_num_stones_after_blinks(num_blinks-1, 1)
    elif (get_num_digits(stone_number) & 1 == 0):
        digits = get_digits(stone_number)
        half_p = (len(digits) // 2)
        return (
            get_num_stones_after_blinks(num_blinks-1, get_num(digits[:half_p])) +
            get_num_stones_after_blinks(num_blinks-1, get_num(digits[half_p:]))
        )
    else:
        return get_num_stones_after_blinks(num_blinks-1, stone_number*2024)

def print_stones(start_stone):
    while (start_stone is not None):
        print(start_stone, end=" ")
        start_stone = start_stone.after
    print("\n\n")

def part1(filename):
    content = read_file(filename)
    stones = parse.parse_list(content, int)
    start_stone = construct_dll(stones)
    NUM_BLINKS = 25
    num_stones = 0
    while (start_stone is not None):
        num_stones += get_num_stones_after_blinks(NUM_BLINKS, start_stone.val)
        start_stone = start_stone.after
    return num_stones

def part2(filename):
    content = read_file(filename)
    stones = parse.parse_list(content, int)
    start_stone = construct_dll(stones)
    NUM_BLINKS = 75
    num_stones = 0
    while (start_stone is not None):
        num_stones += get_num_stones_after_blinks(NUM_BLINKS, start_stone.val)
        start_stone = start_stone.after
    return num_stones

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
        out = 55312
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = None
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "11"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
