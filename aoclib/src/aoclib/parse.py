def parse_list(content, func=None, delim=" "):
    if (func is None):
        content_as_list = content.split(delim)
    else:
        content_as_list = list(map(func, content.split(delim)))
    return content_as_list

def parse_matrix(content, func=None, col_delim=" ", row_delim="\n"):
    rows = content.split(row_delim)
    matrix = [parse_list(row, func, col_delim) for row in rows]
    return matrix
