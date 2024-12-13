import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def construct_matrix(content):
    rows = content.split("\n")
    rows = [list(row) for row in rows]
    return rows

def get_guard_pos(matrix):
    GUARD = set(["<", "^", ">", "v"])
    M = len(matrix)
    N = len(matrix[0])
    for (i, j) in it.product(range(M), range(N)):
        if (matrix[i][j] in GUARD):
            return (i, j)

def is_in_bounds(matrix, pos):
    return (
        (0 <= pos[0] < len(matrix)) and 
        (0 <= pos[1] < len(matrix[0]))
    )

def simulate_guard(matrix, guard_pos):
    OBSTACLE = "#"
    EMPTY = "."
    MARKER = "X"
    DIRECTION_TO_DELTA = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1)
    }
    DIRECTION_TO_TURN = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^"
    }
    guard_visited = set()
    while (True):
        guard_pos_i = guard_pos[0]
        guard_pos_j = guard_pos[1]
        guard_dir = matrix[guard_pos_i][guard_pos_j]
        if ((guard_pos, guard_dir) in guard_visited):
            return -1
        else:
            guard_visited.add((guard_pos, guard_dir))
        delta = DIRECTION_TO_DELTA[guard_dir]
        i_delta = delta[0]
        j_delta = delta[1]
        new_guard_pos_i = (guard_pos_i + i_delta)
        new_guard_pos_j = (guard_pos_j + j_delta)
        new_guard_pos = (new_guard_pos_i, new_guard_pos_j)
        if (not is_in_bounds(matrix, new_guard_pos)):
            break
        if (matrix[new_guard_pos_i][new_guard_pos_j] == OBSTACLE):
            new_guard_dir = DIRECTION_TO_TURN[guard_dir]
            matrix[guard_pos_i][guard_pos_j] = new_guard_dir
        else:
            matrix[guard_pos_i][guard_pos_j] = MARKER
            matrix[new_guard_pos_i][new_guard_pos_j] = guard_dir
            guard_pos = new_guard_pos
    # Cannot be a loop
    guard_pos_i = guard_pos[0]
    guard_pos_j = guard_pos[1]
    guard_dir = matrix[guard_pos_i][guard_pos_j]
    guard_visited.add((guard_pos, guard_dir))
    matrix[guard_pos_i][guard_pos_j] = MARKER
    return set([visited_pos for (visited_pos, visited_dir) in guard_visited])

def add_obstruction(matrix, pos):
    OBSTACLE = "#"
    matrix[pos[0]][pos[1]] = OBSTACLE

def remove_obstruction(matrix, pos):
    EMPTY = "."
    matrix[pos[0]][pos[1]] = EMPTY

def reset_guard(matrix, orig_direction, orig_pos):
    matrix[orig_pos[0]][orig_pos[1]] = orig_direction

def get_distinct_count(matrix):
    MARKER = "X"
    return sum([sum([1 if (cell == MARKER) else 0 for cell in row]) for row in matrix])

def main(filename):
    content = read_file(filename)
    matrix = construct_matrix(content)
    guard_pos = get_guard_pos(matrix)
    orig_direction = matrix[guard_pos[0]][guard_pos[1]]
    guard_visited = simulate_guard(matrix, guard_pos)
    reset_guard(matrix, orig_direction, guard_pos)
    valid_obstruction_count = 0
    for obstruction_pos in guard_visited:
        if (obstruction_pos == guard_pos):
            continue
        add_obstruction(matrix, obstruction_pos)
        obstructed_visited = simulate_guard(matrix, guard_pos)
        reset_guard(matrix, orig_direction, guard_pos)
        if (obstructed_visited == -1):
            valid_obstruction_count += 1
        remove_obstruction(matrix, obstruction_pos)
    return valid_obstruction_count
    #return get_distinct_count(matrix)

class Test(unittest.TestCase):
    filename = "6.small.in"

    def test_1_small(self):
        out = 6
        self.assertEqual(main(self.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    unittest.main(exit=False)
    result = main("6.in")
    pprint(result)
