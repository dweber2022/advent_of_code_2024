from aoclib import parse, convert
from collections import deque
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_pos_of_obj(matrix, obj):
    for (pos, val) in matrix.items():
        if (val == obj):
            return pos

def get_direction_delta(direction):
    DIRECTION_TO_DELTA = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1)
    }
    return DIRECTION_TO_DELTA[direction]

def get_direction_rotations(direction):
    DIRECTION_TO_ROTATIONS = {
        "^": ("<", ">"),
        ">": ("^", "v"),
        "v": (">", "<"),
        "<": ("v", "^")
    }
    return DIRECTION_TO_ROTATIONS[direction]

def get_new_pos(pos, delta):
    return (pos[0]+delta[0], pos[1]+delta[1])

def is_in_bounds(matrix, pos):
    WALL = "#"
    invalid = set([WALL, None])
    return (not matrix[pos] in invalid)

def get_lowest_score(matrix, start_pos, end_pos):
    queue = deque([(start_pos, ">", 0)])
    visited = set()
    visited_to_score = dict()
    min_score = float("inf")
    while (queue):
        payload = queue.popleft()
        pos = payload[0]
        direction = payload[1]
        score = payload[2]
        if (pos == end_pos):
            min_score = min(min_score, score)
            continue
        elif (
            ((pos, direction) in visited) and
            (score >= visited_to_score[(pos, direction)]) 
        ):
            continue
        visited.add((pos, direction))
        visited_to_score[(pos, direction)] = score
        delta = get_direction_delta(direction)
        new_pos = get_new_pos(pos, delta)
        if (is_in_bounds(matrix, new_pos)):
            payload = (new_pos, direction, score+1)
            queue.append(payload)
        for new_direction in get_direction_rotations(direction):
            payload = (pos, new_direction, score+1000)
            queue.append(payload)
    return min_score

def get_lowest_paths(matrix, lowest_score, start_pos, end_pos):
    queue = deque([(start_pos, ">", 0, list())])
    visited = set()
    visited_to_score = dict()
    lowest_paths = list()
    while (queue):
        payload = queue.popleft()
        pos = payload[0]
        direction = payload[1]
        score = payload[2]
        path = payload[3]
        if (score > lowest_score):
            continue
        if (pos == end_pos):
            path.append(end_pos)
            lowest_paths.append(path)
            continue
        elif (
            ((pos, direction) in visited) and
            (score > visited_to_score[(pos, direction)]) 
        ):
            continue
        visited.add((pos, direction))
        visited_to_score[(pos, direction)] = score
        delta = get_direction_delta(direction)
        new_pos = get_new_pos(pos, delta)
        if (is_in_bounds(matrix, new_pos)):
            payload = (new_pos, direction, score+1, path+[pos])
            queue.append(payload)
        for new_direction in get_direction_rotations(direction):
            payload = (pos, new_direction, score+1000, path)
            queue.append(payload)
    return lowest_paths

def part1(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    START = "S"
    END = "E"
    start_pos = get_pos_of_obj(matrix, START)
    end_pos = get_pos_of_obj(matrix, END)
    return get_lowest_score(matrix, start_pos, end_pos)

def part2(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    START = "S"
    END = "E"
    start_pos = get_pos_of_obj(matrix, START)
    end_pos = get_pos_of_obj(matrix, END)
    lowest_score = get_lowest_score(matrix, start_pos, end_pos)
    lowest_paths = get_lowest_paths(matrix, lowest_score, start_pos, end_pos)
    lowest_paths_tiles = set()
    for lowest_path in lowest_paths:
        lowest_paths_tiles = lowest_paths_tiles.union(set(lowest_path))
    return len(lowest_paths_tiles)

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
        out = 11048
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 64
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "16"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
