from aoclib import parse
import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def expand_format(dense_format):
    expanded_format = list()
    file_id = 0
    EMPTY = "."
    for i in range(len(dense_format)):
        block_count = dense_format[i]
        is_file_block = (i & 1 == 0)
        if (is_file_block):
            expanded_format.extend([file_id] * block_count)
            file_id += 1
        else:
            expanded_format.extend([EMPTY] * block_count)
    return expanded_format

def defragment_blocks(expanded_format):
    expanded_format = list(expanded_format)
    lp = 0
    rp = (len(expanded_format) - 1)
    EMPTY = "."
    while (lp < rp):
        while ((lp < rp) and (expanded_format[lp] != EMPTY)):
            lp += 1
        while ((rp > lp) and (expanded_format[rp] == EMPTY)):
            rp -= 1
        expanded_format[lp] = expanded_format[rp]
        expanded_format[rp] = EMPTY
        lp += 1
        rp -= 1
    return expanded_format

def defragment_files(expanded_format):
    def find_leftmost_empty_span(blocks_needed, stop_idx):
        EMPTY = "."
        lp = 0
        rp = 0
        cur_empty_blocks = 0
        while (rp < stop_idx):
            if (expanded_format[rp] == EMPTY):
                cur_empty_blocks += 1
                rp += 1
            elif (cur_empty_blocks < blocks_needed):
                cur_empty_blocks = 0
                rp += 1
                lp = rp
            else:
                return lp
        if (cur_empty_blocks >= blocks_needed):
            return lp
        else:
            return -1

    def grab_file(file_end_p):
        file_id = expanded_format[file_end_p]
        file_start_p = file_end_p
        while (
            (file_start_p > 0) and 
            (expanded_format[file_start_p] == file_id)
        ):
            file_start_p -= 1
        return (file_start_p + 1)

    def move_file(source_start_p, dest_start_p, num_blocks):
        EMPTY = "."
        for _ in range(num_blocks):
            expanded_format[dest_start_p] = expanded_format[source_start_p]
            expanded_format[source_start_p] = EMPTY
            source_start_p += 1
            dest_start_p += 1

    EMPTY = "."
    rp = (len(expanded_format) - 1)
    while (rp > 0):
        while ((rp > 0) and (expanded_format[rp] == EMPTY)):
            rp -= 1
        file_start_p = grab_file(rp)
        blocks_needed = (rp - file_start_p + 1)
        span_start_p = find_leftmost_empty_span(blocks_needed, file_start_p)
        if (span_start_p != -1):
            move_file(file_start_p, span_start_p, blocks_needed)
        rp = (file_start_p - 1)
    return expanded_format

def get_checksum(expanded_format):
    EMPTY = "."
    filled_blocks = filter(lambda p: (p[1] != EMPTY), enumerate(expanded_format))
    return sum(map(lambda p: (p[0] * p[1]), filled_blocks))

def part1(filename):
    dense_format = list(map(int, read_file(filename)))
    expanded_format = expand_format(dense_format)
    expanded_format = defragment_blocks(expanded_format)
    return get_checksum(expanded_format)

def part2(filename):
    dense_format = list(map(int, read_file(filename)))
    expanded_format = expand_format(dense_format)
    expanded_format = defragment_files(expanded_format)
    print(expanded_format)
    return get_checksum(expanded_format)

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
        out = 1928
        self.assertEqual(part1(Test.filename), out)

    def test_2_small(self):
        out = 2858
        self.assertEqual(part2(Test.filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    day = "9"
    small_filename = f"{day}.small.in"
    filename = f"{day}.in"
    Test.set_filename(small_filename)
    unittest.main(exit=False)
    results = main(filename)
    pprint(results)
