from aoclib import parse, convert
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

class Robot:
    def __init__(self, desc):
        self.pos = self.parse_pair(desc[0])
        self.velocity = self.parse_pair(desc[1])

    def parse_pair(self, desc):
        pair = desc.split(",")
        first = int(pair[0][2:])
        second = int(pair[1])
        return (first, second)

    def __str__(self):
        return f"P: {self.pos}, V: {self.velocity}"

def get_new_pos(pos, delta):
    return (pos[0]+delta[0], pos[1]+delta[1])

def wrap_pos(dimensions, pos):
    return (
        (pos[0] % dimensions[0]),
        (pos[1] % dimensions[1])
    )

def simulate_robots(dimensions, robots, num_seconds):
    for robot in robots:
        pos_delta = (robot.velocity[0]*num_seconds, robot.velocity[1]*num_seconds)
        new_pos = get_new_pos(robot.pos, pos_delta)
        new_pos = wrap_pos(dimensions, new_pos)
        robot.pos = new_pos

def draw_robots(dimensions, robots):
    matrix = [[" " for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    for robot in robots:
        pos = robot.pos
        matrix[pos[0]][pos[1]] = "X"
    [print("".join(r)) for r in matrix]

def get_total_pairwise_distance(robots):
    total_distance = 0
    for robot in robots:
        for other_robot in robots:
            total_distance += abs(other_robot.pos[1] - robot.pos[1])
            total_distance += abs(other_robot.pos[0] - robot.pos[0])
    return total_distance

def simulate_robots_slow(dimensions, robots, num_seconds):
    STEP = 101 # determined from output
    for robot in robots:
        pos_delta = (robot.velocity[0]*115, robot.velocity[1]*115)
        new_pos = get_new_pos(robot.pos, pos_delta)
        new_pos = wrap_pos(dimensions, new_pos)
        robot.pos = new_pos
    for t in range(115, num_seconds, STEP): # pattern begins from 115 onwards
        pprint(f"TIME: {t}")
        draw_robots(dimensions, robots)
        for robot in robots:
            pos_delta = (robot.velocity[0]*STEP, robot.velocity[1]*STEP)
            new_pos = get_new_pos(robot.pos, pos_delta)
            new_pos = wrap_pos(dimensions, new_pos)
            robot.pos = new_pos
    pprint(f"TIME: {num_seconds}")
    draw_robots(dimensions, robots)

def get_quadrant_counts(dimensions, robots):
    quadrant_counts = ([0] * 4)
    for robot in robots:
        # ugly but functional
        if (robot.pos[0] < (dimensions[0] // 2)):
            if (robot.pos[1] < (dimensions[1] // 2)):
                quadrant_counts[1] += 1
            elif (robot.pos[1] > (dimensions[1] // 2)):
                quadrant_counts[2] += 1
        elif (robot.pos[0] > (dimensions[0] // 2)):
            if (robot.pos[1] < (dimensions[1] // 2)):
                quadrant_counts[0] += 1
            elif (robot.pos[1] > (dimensions[1] // 2)):
                quadrant_counts[3] += 1
    return quadrant_counts

def part1(filename, width, height):
    content = read_file(filename)
    robots = [Robot(desc) for desc in parse.parse_matrix(content)]
    num_seconds = 100
    simulate_robots((width, height), robots, num_seconds)
    quadrant_counts = get_quadrant_counts((width, height), robots)
    return ft.reduce(lambda x, y: (x * y), quadrant_counts, 1)

def part2(filename, width, height):
    content = read_file(filename)
    robots = [Robot(desc) for desc in parse.parse_matrix(content)]
    num_seconds = 10000000 # or some other high number
    simulate_robots_slow((width, height), robots, num_seconds)

def main(filename, width, height):
    return (
        part1(filename, width, height),
        part2(filename, width, height)
    )

class Test(unittest.TestCase):
    filename = ""

    @staticmethod
    def set_filename(filename):
        Test.filename = filename

    def test_1_small(self):
        out = 12
        self.assertEqual(part1(Test.filename, width=11, height=7), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "14"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename, width=101, height=103)
    pprint(results)
