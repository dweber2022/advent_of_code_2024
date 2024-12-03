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

if __name__ == "__main__":
    unittest.main()
    result = main()
    print(result)
