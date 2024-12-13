from aoclib import parse 
from collections import defaultdict
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_antenna_locations(matrix):
    EMPTY = "."
    m = len(matrix)
    n = len(matrix[0])
    locations = defaultdict(list)
    for (i, j) in it.product(range(m), range(n)):
        cell = matrix[i][j]
        if (cell == EMPTY):
            continue
        locations[cell].append((i, j))
    return locations

def get_slope(start_location, end_location):
    return (
        (end_location[0] - start_location[0]),
        (end_location[1] - start_location[1])
    )

def get_antinode_location(antenna_location, slope):
    return (
        (antenna_location[0] + slope[0]),
        (antenna_location[1] + slope[1])
    )

def get_antinode_pair_locations(antenna_locations):
    antinode_locations = set()
    for (frequency, locations) in antenna_locations.items():
        for (start_location, end_location) in it.combinations(locations, 2):
            slope = get_slope(start_location, end_location)
            negative_slope = tuple(map(lambda x: -x, slope))
            antinode_locations.add(get_antinode_location(start_location, negative_slope))
            antinode_locations.add(get_antinode_location(end_location, slope))
    return antinode_locations

def apply_slope(location, slope):
    return (
        (location[0] + slope[0]),
        (location[1] + slope[1])
    )

def get_antinode_locations(bounds, antenna_locations):
    antinode_locations = set()
    for (frequency, locations) in antenna_locations.items():
        for (start_location, end_location) in it.combinations(locations, 2):
            slope = get_slope(start_location, end_location)
            negative_slope = tuple(map(lambda x: -x, slope))
            while (is_in_bounds(bounds, start_location)):
                antinode_locations.add(start_location)
                start_location = apply_slope(start_location, negative_slope)
            while (is_in_bounds(bounds, end_location)):
                antinode_locations.add(end_location)
                end_location = apply_slope(end_location, slope)
    return antinode_locations
            
def is_in_bounds(bounds, location):
    return (
        (0 <= location[0] < bounds[0]) and
        (0 <= location[1] < bounds[1])
    )

def part1(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    m = len(matrix)
    n = len(matrix[0])
    antenna_locations = get_antenna_locations(matrix)
    antinode_locations = list(filter(lambda location: is_in_bounds((m, n), location), get_antinode_pair_locations(antenna_locations)))
    return len(antinode_locations)

def part2(filename):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    m = len(matrix)
    n = len(matrix[0])
    antenna_locations = get_antenna_locations(matrix)
    antinode_locations = get_antinode_locations((m, n), antenna_locations)
    return len(antinode_locations)

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
        out = 14
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 34
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "8"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
