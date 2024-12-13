from aoclib import parse, convert
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class Region:
    def __init__(self, type, num_sides, area, perimeter):
        self.type = type
        self.num_sides = num_sides
        self.area = area
        self.perimeter = perimeter

def get_new_pos(pos, delta):
    pos_i = pos[0]
    pos_j = pos[1]
    i_delta = delta[0]
    j_delta = delta[1]
    return (pos_i+i_delta, pos_j+j_delta)

def get_region_plots(matrix, region_type, pos):
    DELTAS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    )
    stack = [pos]
    visited = set()
    while (stack):
        pos = stack.pop(-1)
        if (pos in visited):
            continue
        visited.add(pos)
        for delta in DELTAS:
            new_pos = get_new_pos(pos, delta)
            if (matrix[new_pos] == region_type):
                stack.append(new_pos)
    return visited

def get_num_corners(matrix, region_type, pos):
    OUTER_CORNER_DELTAS = (
        ((0, -1), (-1, 0)),
        ((-1, 0), (0, 1)),
        ((0, 1), (1, 0)),
        ((1, 0), (0, -1))
    )
    num_corners = 0
    for corner in OUTER_CORNER_DELTAS:
        is_corner = True
        for delta in corner:
            new_pos = get_new_pos(pos, delta)
            if (matrix[new_pos] == region_type):
                is_corner = False
                break
        if (is_corner):
            num_corners += 1
    INNER_CORNER_DELTAS = (
        ((-1, 0), (-1, 1), (0, 1)),
        ((0, 1), (1, 1), (1, 0)),
        ((1, 0), (1, -1), (0, -1)),
        ((0, -1), (-1, -1), (-1, 0))
    )
    for corner in INNER_CORNER_DELTAS:
        adjacent_delta1 = corner[0]
        adjacent_pos1 = get_new_pos(pos, adjacent_delta1)
        adjacent_delta2 = corner[2]
        adjacent_pos2 = get_new_pos(pos, adjacent_delta2)
        diagonal_delta = corner[1]
        diagonal_pos = get_new_pos(pos, diagonal_delta)
        if (
            (matrix[adjacent_pos1] == matrix[adjacent_pos2] == region_type) and
            (matrix[diagonal_pos] != region_type)
        ):
            num_corners += 1
    return num_corners

def get_region_num_sides(matrix, region_type, pos):
    DELTAS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    )
    num_sides = 0
    stack = [pos]
    visited = set()
    while (stack):
        pos = stack.pop(-1)
        if (pos in visited):
            continue
        visited.add(pos)
        num_sides += get_num_corners(matrix, region_type, pos)
        for delta in DELTAS:
            new_pos = get_new_pos(pos, delta)
            if (matrix[new_pos] == region_type):
                stack.append(new_pos)
    return num_sides

def get_region_perimeter(matrix, region_type, plots):
    DELTAS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    )
    region_perimeter = 0
    for pos in plots:
        for (i_delta, j_delta) in DELTAS:
            new_pos = (pos[0]+i_delta, pos[1]+j_delta)
            if (matrix[new_pos] != region_type):
                region_perimeter += 1
    return region_perimeter

def get_region(matrix, pos):
    SEARCHED = "."
    if (matrix[pos] == SEARCHED):
        return None
    region_type = matrix[pos]
    region_plots = get_region_plots(matrix, region_type, pos)
    region_num_sides = get_region_num_sides(matrix, region_type, pos)
    region_area = len(region_plots)
    region_perimeter = get_region_perimeter(matrix, region_type, region_plots) 
    for pos in region_plots:
        matrix[pos] = SEARCHED
    return Region(region_type, region_num_sides, region_area, region_perimeter)

def get_regions(matrix):
    regions = map(lambda pos: get_region(matrix, pos), list(matrix.keys()))
    regions = filter(lambda region: (region is not None), regions)
    return regions

def part1(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    regions = get_regions(matrix)
    total_fence_cost = sum([(region.area * region.perimeter) for region in regions])
    return total_fence_cost

def part2(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    regions = get_regions(matrix)
    total_fence_cost = sum([(region.area * region.num_sides) for region in regions])
    return total_fence_cost

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
        out = 1930
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 1206
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "12"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
