from aoclib import parse, convert, graph
from collections import defaultdict
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = defaultdict(list)
        self.is_end = False

def construct_patterns(patterns):
    root = TrieNode("")
    cur = root
    for pattern in patterns:
        cur = root
        for color in pattern:
            node = TrieNode(color)
            cur.children[color].append(node)
            cur = node
        cur.is_end = True
    return root

@ft.cache
def is_possible_design(before_root_color, design, prev_color=None, at=0):
    if (at == len(design)):
        return prev_color.is_end
    design_color = design[at]
    if (prev_color is None):
        prev_color = before_root_color
    elif (
        (len(prev_color.children[design_color]) == 0) and
        prev_color.is_end 
    ):
        prev_color = before_root_color
    if (prev_color.children[design_color]):
        next_colors = prev_color.children[design_color]
        for next_color in next_colors:
            if (is_possible_design(before_root_color, design, next_color, at+1)):
                return True
    return False

def get_num_design_comps(before_root_color, design):
    @ft.cache
    def dfs(prev_color=None, at=0):
        if (at == len(design)):
            if (prev_color.is_end):
                return 1
            else:
                return 0
        design_color = design[at]
        if (prev_color is None):
            prev_color = before_root_color
        elif (
            (len(prev_color.children[design_color]) == 0) and
            prev_color.is_end 
        ):
            prev_color = before_root_color
        if (prev_color.children[design_color]):
            next_colors = prev_color.children[design_color]
            num_comps = 0
            for next_color in next_colors:
                num_comps += dfs(next_color, at+1)
            return num_comps
        return 0

    num_comps = dfs()
    return num_comps

def part1(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, row_delim="\n\n", col_delim="\n")
    before_root_pattern_color = construct_patterns(map(lambda pattern: pattern.strip(), payload[0][0].split(",")))
    designs = payload[1]
    possible_designs = list(filter(lambda design: is_possible_design(before_root_pattern_color, design), designs))
    return len(possible_designs)

def part2(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, row_delim="\n\n", col_delim="\n")
    before_root_pattern_color = construct_patterns(map(lambda pattern: pattern.strip(), payload[0][0].split(",")))
    designs = payload[1]
    possible_designs = list(filter(lambda design: is_possible_design(before_root_pattern_color, design), designs))
    return sum(map(lambda design: get_num_design_comps(before_root_pattern_color, design), possible_designs))

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
        out = 6
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 16
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "19"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
