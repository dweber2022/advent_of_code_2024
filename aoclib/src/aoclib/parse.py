def parse_list(content, func=None, delim=" "):
    if (func is None):
        content_as_list = content.split(delim)
    else:
        content_as_list = list(map(func, content.split(delim)))
    return content_as_list
