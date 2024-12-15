from aoclib import parse, convert
from collections import deque
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_robot_pos(matrix):
    ROBOT = "@"
    for (pos, obj) in matrix.items():
        if (obj == ROBOT):
            return pos

def get_new_pos(pos, move):
    MOVE_TO_DELTA = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1)
    }
    delta = MOVE_TO_DELTA[move]
    return (pos[0]+delta[0], pos[1]+delta[1])

def get_new_pos_delta(pos, delta):
    return (pos[0]+delta[0], pos[1]+delta[1])

def is_in_bounds(matrix, pos):
    return (matrix[pos] is not None)

def move_box_in_direction(matrix, box_pos, move):
    BOX = "O"
    WALL = "#"
    EMPTY = "."
    source_box_pos = box_pos
    dest_box_pos = box_pos
    while (is_in_bounds(matrix, dest_box_pos)):
        dest_box_pos = get_new_pos(dest_box_pos, move)
        if (matrix[dest_box_pos] == EMPTY):
            matrix[source_box_pos] = EMPTY
            matrix[dest_box_pos] = BOX
            return True
        elif (matrix[dest_box_pos] == WALL):
            return False
    return False

def get_box_poses(matrix, box_pos):
    BOX_START = "["
    BOX_END = "]"
    LEFT_DELTA = (0, -1)
    RIGHT_DELTA = (0, 1)
    if (matrix[box_pos] == BOX_START):
        return (box_pos, get_new_pos_delta(box_pos, RIGHT_DELTA))
    elif (matrix[box_pos] == BOX_END):
        return (box_pos, get_new_pos_delta(box_pos, LEFT_DELTA))

def move_expanded_box_in_direction(matrix, box_pos, move):
    BOX = set(["[", "]"])
    WALL = "#"
    EMPTY = "."
    box_poses = get_box_poses(matrix, box_pos)
    to_move_queue = list()
    visited = set()
    queue = deque(box_poses)
    while (queue):
        box_pos = queue.popleft()
        if (box_pos in visited):
            continue
        visited.add(box_pos)
        to_move_queue.append((box_pos, matrix[box_pos]))
        new_pos = get_new_pos(box_pos, move)
        if (matrix[new_pos] in BOX):
            new_box_poses = get_box_poses(matrix, new_pos)
            queue.extend(new_box_poses)
        elif (matrix[new_pos] == EMPTY):
            continue
        elif (matrix[new_pos] == WALL):
            return False
    while (to_move_queue):
        payload = to_move_queue.pop(-1)
        box_pos = payload[0]
        box_piece = payload[1]
        new_box_pos = get_new_pos(box_pos, move)
        matrix[box_pos] = EMPTY
        matrix[new_box_pos] = box_piece
    return True

def simulate_robot(matrix, robot_pos, robot_moves, expanded=False):
    WALL = "#"
    BOX = set(["O", "[", "]"])
    EMPTY = "."
    ROBOT = "@"
    for move in robot_moves:
        new_robot_pos = get_new_pos(robot_pos, move)
        if (not is_in_bounds(matrix, new_robot_pos)):
            continue
        elif (matrix[new_robot_pos] == WALL):
            continue
        elif (matrix[new_robot_pos] in BOX):
            if (expanded):
                move_success = move_expanded_box_in_direction(matrix, new_robot_pos, move)
            else:
                move_success = move_box_in_direction(matrix, new_robot_pos, move)
            if (not move_success):
                continue
        matrix[new_robot_pos] = ROBOT
        matrix[robot_pos] = EMPTY
        robot_pos = new_robot_pos

def get_box_gps(box_pos):
    return ((100 * box_pos[0]) + box_pos[1])

def get_alL_box_gps(matrix, expanded=False):
    if (expanded):
        BOX = "["
    else:
        BOX = "O"
    gps = list()
    for (pos, obj) in matrix.items():
        if (obj == BOX):
            gps.append(get_box_gps(pos))
    return gps

def get_expanded_matrix(matrix):
    OBJECT_TO_EXPANDED = {
        "#": ("#", "#"),
        "O": ("[", "]"),
        ".": (".", "."),
        "@": ("@", ".")
    }
    m = len(matrix)
    n = len(matrix[0])
    new_matrix = [[None for _ in range(2*n)] for _ in range(m)]
    for (i, j) in it.product(range(m), range(n)):
        expanded = OBJECT_TO_EXPANDED[matrix[i][j]]
        new_matrix[i][2*j] = expanded[0]
        new_matrix[i][2*j+1] = expanded[1]
    return new_matrix

def print_matrix(matrix):
    m = max(map(lambda p: (p[0] + 1), matrix.keys()))
    n = max(map(lambda p: (p[1] + 1), matrix.keys()))
    grid = [[None for _ in range(n)] for _ in range(m)]
    for (i, j) in matrix.keys():
        grid[i][j] = matrix[(i, j)]
    [print("".join(r)) for r in grid]

def part1(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, row_delim="\n\n")
    matrix = parse.parse_matrix(payload[0][0], col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    robot_moves = list(filter(lambda m: (m != "\n"), parse.parse_list(payload[1][0], delim="")))
    robot_pos = get_robot_pos(matrix)
    simulate_robot(matrix, robot_pos, robot_moves)
    all_box_gps = get_alL_box_gps(matrix)
    return sum(all_box_gps)

def part2(filename):
    content = read_file(filename)
    payload = parse.parse_matrix(content, row_delim="\n\n")
    matrix = parse.parse_matrix(payload[0][0], col_delim="")
    matrix = get_expanded_matrix(matrix)
    matrix = convert.convert_to_dict_matrix(matrix)
    robot_moves = list(filter(lambda m: (m != "\n"), parse.parse_list(payload[1][0], delim="")))
    robot_pos = get_robot_pos(matrix)
    simulate_robot(matrix, robot_pos, robot_moves, expanded=True)
    all_box_gps = get_alL_box_gps(matrix, expanded=True)
    return sum(all_box_gps)

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
        out = 10092
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 9021
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "15"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
