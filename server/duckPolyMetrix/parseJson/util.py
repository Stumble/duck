# this function will remove all "class " in the string
# input: str
# rtn  : str
def remove_class_prefix(full_name):
    rtn = ""
    while True:
        (before, cls, after) = full_name.partition('class ')
        rtn += before
        if after:
            full_name = after
        else:
            break
    return rtn
