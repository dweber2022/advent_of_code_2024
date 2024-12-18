from aoclib import parse, convert, graph
from collections import deque
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def construct_matrix(dimensions):
    EMPTY = "."
    matrix = [[EMPTY for _ in range(dimensions[1]+1)] for _ in range(dimensions[0]+1)]
    matrix = convert.convert_to_dict_matrix(matrix)
    return matrix

def simulate_bytes(matrix, byte_positions):
    BYTE = "#"
    for pos in byte_positions:
        matrix[pos] = BYTE

def get_path(matrix, start_pos, end_pos):
    BYTE = "#"
    DIRECTIONS = ("^", ">", "v", "<")
    queue = deque([(start_pos, list())])
    visited = set()
    while (queue):
        payload = queue.popleft()
        pos = payload[0]
        path = payload[1]
        if (pos == end_pos):
            return path
        elif (pos in visited):
            continue
        visited.add(pos)
        for direction in DIRECTIONS:
            delta = graph.get_direction_delta(direction)
            new_pos = graph.get_new_pos(pos, delta)
            if (
                graph.is_in_bounds(matrix, new_pos) and 
                matrix[new_pos] != BYTE
            ):
                queue.append((new_pos, path+[pos]))
    return list()

def get_first_blocking_byte_pos(matrix, byte_positions, start_pos, end_pos):
    for pos in byte_positions:
        matrix[pos] = "#"
        path = get_path(matrix, start_pos, end_pos)
        if (len(path) == 0):
            return pos
    return (-1, -1)

def part1(filename, dimensions, num_bytes):
    content = read_file(filename)
    byte_positions = [tuple(map(int, pos.split(","))) for pos in parse.parse_list(content, delim="\n")]
    matrix = construct_matrix(dimensions)
    simulate_bytes(matrix, byte_positions[:num_bytes])
    START_POS = (0, 0)
    END_POS = dimensions
    path = get_path(matrix, START_POS, END_POS)
    return len(path)

def part2(filename, dimensions, num_bytes):
    content = read_file(filename)
    byte_positions = [tuple(map(int, pos.split(","))) for pos in parse.parse_list(content, delim="\n")]
    matrix = construct_matrix(dimensions)
    simulate_bytes(matrix, byte_positions[:num_bytes])
    START_POS = (0, 0)
    END_POS = dimensions
    return get_first_blocking_byte_pos(matrix, byte_positions[num_bytes:], START_POS, END_POS)

def main(filename):
    return (
        part1(filename, (70, 70), 1024),
        part2(filename, (70, 70), 1024)
    )

class Test(unittest.TestCase):
    filename = ""

    @staticmethod
    def set_filename(filename):
        Test.filename = filename

    def test_1_small(self):
        out = 22
        self.assertEqual(part1(Test.filename, (6, 6), 12), out)

    def test_2_small(self):
        out = (6, 1)
        self.assertEqual(part2(Test.filename, (6, 6), 12), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "18"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
