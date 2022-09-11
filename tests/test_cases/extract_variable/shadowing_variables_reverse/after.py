def inline_inside_me():
    rename_me = 4 + 1
    return rename_me + 3


def no_variables_should_be_inlined_inside_me():
    return 4 + 1 + 3
