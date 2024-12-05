# Start: 50 minutes late
# End:

from collections import defaultdict
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def construct_adj_matrix(directed_edges):
    adj_matrix = defaultdict(set)
    for (start, end) in directed_edges:
        adj_matrix[start].add(end)
    return adj_matrix

def is_correct_update(adj_matrix, update):
    for (before_page, after_page) in it.pairwise(update):
        if (not after_page in adj_matrix[before_page]):
            return False
    return True

def get_correct_update(adj_matrix, incorrect_update):
    page_to_num_successors = defaultdict(int)
    for (page1, page2) in it.combinations(incorrect_update, 2):
        if (page2 in adj_matrix[page1]):
            page_to_num_successors[page1] += 1
        elif (page1 in adj_matrix[page2]):
            page_to_num_successors[page2] += 1
    correct_update = list(map(lambda x: x[0], sorted(page_to_num_successors.items(), key=lambda x: -x[1])))
    return correct_update

def main(filename):
    content = read_file(filename)
    payload = content.split("\n\n")
    directed_edges = [list(map(int, edge.split("|"))) for edge in payload[0].split("\n")]
    updates = [list(map(int, update.split(","))) for update in payload[1].split("\n")]
    adj_matrix = construct_adj_matrix(directed_edges)
    #correct_updates = filter(lambda update: is_correct_update(adj_matrix, update), updates)
    incorrect_updates = filter(lambda update: (not is_correct_update(adj_matrix, update)), updates)
    correct_updates = list(map(lambda update: get_correct_update(adj_matrix, update), incorrect_updates))
    return sum([update[len(update)//2] for update in correct_updates])

class Test(unittest.TestCase):
    filename = "5.small.in"

    def test_1_small(self):
        out = 123
        self.assertEqual(main(self.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    unittest.main(exit=False)
    result = main("5.in")
    pprint(result)
