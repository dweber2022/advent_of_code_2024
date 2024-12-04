from itertools import product
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def get_xmas_count(matrix, pos):
    WORD = "XMAS"
    pos_i = pos[0]
    pos_j = pos[1]
    if (not matrix[pos_i][pos_j].startswith(WORD[0])):
        return 0 
    MOVES = [
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (-1, 0),
        (0, -1)
    ]
    xmas_count = 0
    for (i_delta, j_delta) in MOVES:
        p = 1
        new_i = pos_i
        new_j = pos_j
        while (p < len(WORD)):
            new_i += i_delta
            new_j += j_delta
            if ((new_i < 0) or (new_i >= len(matrix))):
                break
            if ((new_j < 0) or (new_j >= len(matrix[0]))):
                break
            if (matrix[new_i][new_j] != WORD[p]):
                break
            p += 1
        if (p == len(WORD)):
            xmas_count += 1
    return xmas_count

def is_x_mas(matrix, pos):
    pos_i = pos[0]
    pos_j = pos[1]
    center = "A"
    if (not matrix[pos_i][pos_j].startswith(center)):
        return False
    if ((pos_i < 1) or (pos_i >= (len(matrix)-1))):
        return False
    if ((pos_j < 1) or (pos_j >= (len(matrix[0])-1))):
        return False
    DIAGONALS = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]
    counts = dict()
    for (i_delta, j_delta) in DIAGONALS:
        new_i = (pos_i + i_delta)
        new_j = (pos_j + j_delta)
        char = matrix[new_i][new_j]
        counts[char] = (counts.get(char, 0) + 1)
    if ((counts.get("M", 0) != 2) or (counts.get("S", 0) != 2)):
        return False
    if (matrix[pos_i+1][pos_j+1] == matrix[pos_i-1][pos_j-1]):
        return False
    if (matrix[pos_i-1][pos_j+1] == matrix[pos_i+1][pos_j-1]):
        return False
    return True

def main(filename):
    content = read_file(filename)
    matrix = content.split()
    m = len(matrix)
    n = len(matrix[0])
    #return sum([get_xmas_count(matrix, pos) for pos in product(range(m), range(n))])
    return sum([is_x_mas(matrix, pos) for pos in product(range(m), range(n))])

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
    
class Test(unittest.TestCase):
    filename = "4.small.in"

    def test_1_small(self):
        out = 9
        self.assertEqual(main(self.filename), out)

if __name__ == "__main__":
    unittest.main(exit=False)
    result = main("4.in")
    pprint(result)
