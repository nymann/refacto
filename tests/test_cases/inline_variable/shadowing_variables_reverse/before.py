def inline_inside_me():
    a = 4 + 1
    return a + 3


def no_variables_should_be_inlined_inside_me():
    a = 4 + 1
    return a + 3
