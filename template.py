import itertools as it
import functools as ft
import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def main(filename):
    content = read_file(filename)

class Test(unittest.TestCase):
    filename = ""

    def test_1_small(self):
        out = None
        self.assertEqual(main(filename), out)

def pprint(message):
    print("="*50, end="\n\n")
    print(f"Output: {message}", end="\n\n")
    print("="*50)
 
if __name__ == "__main__":
    unittest.main(exit=False)
    result = main("")
    pprint(result)
