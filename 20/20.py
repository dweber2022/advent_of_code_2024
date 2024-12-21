from aoclib import parse, convert, graph
from collections import deque
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_path_and_time(matrix, start_pos, end_pos):
    DIRECTIONS = ("^", ">", "v", "<")
    EMPTY = "."
    queue = deque([(start_pos, list(), 0)])
    visited = set()
    while (queue):
        payload = queue.popleft()
        pos = payload[0]
        path = payload[1]
        time = payload[2]
        if (pos == end_pos):
            return (path, time)
        if (
            (pos != start_pos) and 
            (matrix[pos] != EMPTY)
        ):
            continue
        elif (pos in visited):
            continue
        else:
            visited.add(pos)
        for direction in DIRECTIONS:
            delta = graph.get_direction_delta(direction)
            new_pos = graph.get_new_pos(pos, delta)
            if (graph.is_in_bounds(matrix, new_pos)):
                queue.append((new_pos, path+[new_pos], time+1))
    return None

def get_path_time(matrix, start_pos, end_pos):
    if (not hasattr(get_path_time, "cache")):
        get_path_time.cache = dict()
    path_time = get_path_time.cache.get((start_pos, end_pos), None)
    if (path_time is None):
        payload = get_path_and_time(matrix, start_pos, end_pos)
        path_time = payload[1]
        get_path_time.cache[(start_pos, end_pos)] = path_time
        return path_time
    else:
        return path_time

def get_cheat_path_and_time(matrix, start_pos, end_pos):
    DIRECTIONS = ("^", ">", "v", "<")
    WALL = "#"
    queue = deque([(start_pos, list(), 0)])
    visited = set()
    while (queue):
        payload = queue.popleft()
        pos = payload[0]
        path = payload[1]
        time = payload[2]
        if (pos in visited):
            continue
        else:
            visited.add(pos)
        for direction in DIRECTIONS:
            delta = graph.get_direction_delta(direction)
            new_pos = graph.get_new_pos(pos, delta)
            if (not graph.is_in_bounds(matrix, new_pos)):
                continue
            if (
                (pos == start_pos) and
                (matrix[new_pos] != WALL)
            ):
                continue
            elif (
                (matrix[pos] == WALL) and
                (new_pos == end_pos)
            ):
                return (path+[end_pos], time+1)
            else:
                queue.append((new_pos, path+[new_pos], time+1))
    return None

def get_time_to_end(matrix):
    START = "S"
    END = "E"
    start_pos = graph.get_pos_of_obj(matrix, START)
    end_pos = graph.get_pos_of_obj(matrix, END)
    payload = get_path_and_time(matrix, start_pos, end_pos)
    return payload[1]

"""
def get_all_pairs_shortest_distance(matrix):
    DIRECTIONS = ("^", ">", "v", "<")
    WALL = "#"
    adj_matrix = dict()
    empty_poses = list(filter(lambda pos: (matrix[pos] != WALL), matrix.keys()))
    for pos in empty_poses:
        for direction in DIRECTIONS:
            delta = graph.get_direction_delta(direction)
            adj_pos = graph.get_new_pos(pos, delta)
            if (not graph.is_in_bounds(matrix, adj_pos)):
                continue
            elif (matrix[adj_pos] == WALL):
                continue
            else:
                if (adj_matrix.get(pos, None) is None):
                    adj_matrix[pos] = dict()
                if (adj_matrix.get(adj_pos, None) is None):
                    adj_matrix[adj_pos] = dict()
                adj_matrix[pos][adj_pos] = 1
                adj_matrix[adj_pos][pos] = 1
    for k in adj_matrix.keys():
        for i in adj_matrix.keys():
            for j in adj_matrix.keys():
                if (i == j):
                    adj_matrix[i][j] = 0
                    adj_matrix[j][i] = 0
                    continue
                elif (adj_matrix[i].get(k, None) is None):
                    continue
                elif (adj_matrix[k].get(j, None) is None):
                    continue
                adj_matrix[i][j] = min(
                    adj_matrix[i].get(j, float("inf")),
                    (adj_matrix[i][k] + adj_matrix[k][j])
                )
                adj_matrix[j][i] = min(
                    adj_matrix[j].get(i, float("inf")),
                    (adj_matrix[j][k] + adj_matrix[k][i])
                )
    return adj_matrix
"""

def get_cheats_at_pos(matrix, cheat_duration, cheat_start_pos):
    WALL = "#"
    cheats_poses = set()
    total_delta = cheat_duration
    for i_delta in range(-total_delta, total_delta+1):
        remaining_delta = (total_delta - abs(i_delta))
        for j_delta in range(-remaining_delta, remaining_delta+1):
            if ((abs(i_delta) + abs(j_delta)) < 2): # cannot be adjacent to start
                continue
            delta = (i_delta, j_delta)
            cheat_end_pos = graph.get_new_pos(cheat_start_pos, delta)
            if (not graph.is_in_bounds(matrix, cheat_end_pos)):
                continue
            elif (matrix[cheat_end_pos] == WALL):
                continue
            payload = get_cheat_path_and_time(matrix, cheat_start_pos, cheat_end_pos)
            if (payload is None):
                continue
            cheats_poses.add((cheat_start_pos, cheat_end_pos))
    return cheats_poses

def get_manhattan_distance(pos1, pos2):
    return (
        abs(pos1[0] - pos2[0]) +
        abs(pos1[1] - pos2[1])
    )

def is_valid_cheat_time(matrix, maximum_cheat_time_to_end, start_pos, end_pos, cheat_start_pos, cheat_end_pos):
    cheat_time = get_path_time(matrix, start_pos, cheat_start_pos)
    cheat_time += get_manhattan_distance(cheat_start_pos, cheat_end_pos)
    if (cheat_time > maximum_cheat_time_to_end):
        return False
    cheat_time += get_path_time(matrix, cheat_end_pos, end_pos)
    return (cheat_time <= maximum_cheat_time_to_end)

def get_num_good_cheats(matrix, cheat_duration, maximum_cheat_time_to_end):
    WALL = "#"
    START = "S"
    END = "E"
    start_pos = graph.get_pos_of_obj(matrix, START)
    end_pos = graph.get_pos_of_obj(matrix, END)
    num_good_cheats = 0
    cheat_start_poses = list(filter(lambda pos: (matrix[pos] != WALL), matrix.keys()))
    all_cheats = set() 
    c = 1
    for cheat_start_pos in cheat_start_poses:
        pprint(f"evaluated start pos {c/len(cheat_start_poses)} ({100*c/len(cheat_start_poses)})")
        c += 1
        all_cheats = all_cheats.union(get_cheats_at_pos(matrix, cheat_duration, cheat_start_pos))
    num_cheats = (len(all_cheats))
    i = 1
    for (cheat_start_pos, cheat_end_pos) in all_cheats:
        i += 1
        if is_valid_cheat_time(matrix, maximum_cheat_time_to_end, start_pos, end_pos, cheat_start_pos, cheat_end_pos):
            num_good_cheats += 1
            pprint(f"good: {num_good_cheats}\n{cheat_start_pos} {cheat_end_pos} ({i}/{num_cheats}) ({100*i/num_cheats})")
    return num_good_cheats

def part1(filename, minimum_time_saved=100):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    maximum_time_to_end = get_time_to_end(matrix)
    CHEAT_DURATION = 2
    maximum_cheat_time_to_end = (maximum_time_to_end - minimum_time_saved)
    return get_num_good_cheats(matrix, CHEAT_DURATION, maximum_cheat_time_to_end)

def part2(filename, minimum_time_saved=100):
    content = read_file(filename)
    matrix = parse.parse_matrix(content, col_delim="")
    matrix = convert.convert_to_dict_matrix(matrix)
    maximum_time_to_end = get_time_to_end(matrix)
    CHEAT_DURATION = 20
    maximum_cheat_time_to_end = (maximum_time_to_end - minimum_time_saved)
    return get_num_good_cheats(matrix, CHEAT_DURATION, maximum_cheat_time_to_end)

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
        out = 44
        self.assertEqual(part1(Test.filename, 1), out)

    def test_2_small(self):
        out = 285
        self.assertEqual(part2(Test.filename, 50), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "20"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
