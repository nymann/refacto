def no_variables_should_be_inlined_inside_me():
    c = 1 + 2
    return c + 3


def inline_inside_me():
    return 4 + 1 + 2
