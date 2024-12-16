import itertools as it

def get_pos_of_obj(matrix, obj):
    if (isinstance(matrix, dict)):
        for (pos, val) in matrix.items():
            if (val == obj):
                return pos
    else:
        m = len(matrix)
        n = len(matrix[0])
        for (i, j) in it.product(range(m), range(n)):
            if (matrix[i][j] == obj):
                return (i, j)

def is_in_bounds(matrix, pos):
    if (isinstance(matrix, dict)):
        return (matrix[pos] is not None)
    else:
        m = len(matrix)
        n = len(matrix[0])
        return (
            (0 <= pos[0] < m) and
            (0 <= pos[1] < n)
        )

def get_new_pos(pos, delta):
    return (pos[0]+delta[0], pos[1]+delta[1])

def get_direction_delta(direction):
    DIRECTION_TO_DELTA = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1)
    }
    return DIRECTION_TO_DELTA[direction]

