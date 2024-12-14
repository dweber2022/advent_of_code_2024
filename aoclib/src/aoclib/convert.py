from collections import defaultdict

class DoublyLinkedNode:
    def __init__(self, val):
        self.val = val
        self.before = None
        self.after = None

    def __iter__(self):
        return DoublyLinkedListIterator(self)

class DoublyLinkedListIterator:
    def __init__(self, root):
        self.root = root

    def __next__(self):
        if (self.root is None):
            raise StopIteration
        value = self.root.val
        self.root = self.root.after
        return value

def convert_to_doubly_linked_list(l):
    root = None
    prev = None
    for value in l:
        cur = DoublyLinkedNode(value)
        if (root is None):
            root = cur
        else:
            prev.after = cur
            cur.before = prev
        prev = cur
    return root

def convert_to_dict_matrix(matrix):
    m = len(matrix)
    n = len(matrix[0])
    return defaultdict(
        lambda: None,
        { (i, j):matrix[i][j] for i in range(m) for j in range(n) }
    )
