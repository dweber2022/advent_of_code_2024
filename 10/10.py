from aoclib import parse
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_trailheads(matrix):
    m = len(matrix)
    n = len(matrix[0])
    TRAILHEAD = 0
    return list(filter(lambda x: (x != -1), [(i, j) if (matrix[i][j] == TRAILHEAD) else -1 for (i, j) in it.product(range(m), range(n))]))

def is_in_bounds(matrix, pos):
    m = len(matrix)
    n = len(matrix[0])
    return (
        (0 <= pos[0] < m) and
        (0 <= pos[1] < n)
    )

def get_trailends(matrix, trailhead):
    stack = [trailhead]
    TRAILEND = 9
    DELTAS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    ]
    trailends = set()
    trailend_to_rating = dict()
    while (stack):
        cur_pos = stack.pop(-1)
        if (cur_pos in trailends):
            trailend_to_rating[cur_pos] += 1
            continue
        pos_i = cur_pos[0]
        pos_j = cur_pos[1]
        cur_height = matrix[pos_i][pos_j]
        if (cur_height == TRAILEND):
            trailends.add(cur_pos)
            trailend_to_rating[cur_pos] = 1
        for (delta_i, delta_j) in DELTAS:
            new_i = (pos_i + delta_i)
            new_j = (pos_j + delta_j)
            new_pos = (new_i, new_j)
            if (not is_in_bounds(matrix, new_pos)):
                continue
            new_height = matrix[new_i][new_j]
            if (new_height != (cur_height + 1)):
                continue
            stack.append(new_pos)
    return { trailend: trailend_to_rating[trailend] for trailend in trailends }

def part1(filename):
    content = read_file(filename)
    matrix = [list(map(int, list(row[0]))) for row in parse.parse_matrix(content)]
    trailheads = get_trailheads(matrix)
    all_trailends = list(map(lambda trailhead: get_trailends(matrix, trailhead), trailheads))
    num_trailends = sum(map(len, all_trailends))
    return num_trailends


def part2(filename):
    content = read_file(filename)
    matrix = [list(map(int, list(row[0]))) for row in parse.parse_matrix(content)]
    trailheads = get_trailheads(matrix)
    all_trailend_ratings = map(lambda p: sum(p.values()), map(lambda trailhead: get_trailends(matrix, trailhead), trailheads))
    sum_trailend_ratings = sum(all_trailend_ratings)
    return sum_trailend_ratings

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
        out = 36
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 81
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "10"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
